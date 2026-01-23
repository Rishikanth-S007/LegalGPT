import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Paper,
  Typography,
  Tooltip,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ForumIcon from '@mui/icons-material/Forum';
import { useNavigate } from 'react-router-dom';
import RelatedContent from './RelatedContent';

const ChatInterface = ({ serviceType }) => {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [recognition, setRecognition] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    let recognitionInstance = null;
    
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onstart = () => {
        setIsListening(true);
        // Remove any existing system messages about voice input
        setChatMessages(prev => prev.filter(msg => 
          !(msg.sender === 'system' && (
            msg.text.includes('Voice input') || 
            msg.text.includes('Voice recognition')
          ))
        ));
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        
        // Clear previous error messages
        setChatMessages(prev => prev.filter(msg => 
          !(msg.sender === 'system' && msg.text.includes('Voice recognition error'))
        ));

        // Add appropriate error message based on the error type
        let errorMessage = "Voice recognition error. Please try again or type your message.";
        if (event.error === 'not-allowed') {
          errorMessage = "Microphone access denied. Please enable microphone access and try again.";
        } else if (event.error === 'no-speech') {
          // Don't show no-speech error in continuous mode
          return;
        }

        setChatMessages(prev => [...prev, {
          text: errorMessage,
          sender: 'system'
        }]);
      };

      recognitionInstance.onend = () => {
        // Only restart if we're still supposed to be listening
        if (isListening) {
          try {
            recognitionInstance.start();
          } catch (error) {
            console.error('Failed to restart recognition:', error);
            setIsListening(false);
          }
        } else {
          setIsListening(false);
        }
      };

      let finalTranscript = '';
      recognitionInstance.onresult = (event) => {
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript + ' ';
          } else {
            interimTranscript += transcript;
          }
        }

        // Update the input field with both final and interim results
        setMessage(finalTranscript + interimTranscript);
      };

      setRecognition(recognitionInstance);
    }

    return () => {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
    };
  }, [isListening]); // Add isListening to the dependency array

  const formatMessage = (text) => {
    // Handle code blocks
    const formattedText = text.replace(
      /```([\s\S]*?)```/g,
      (match, code) => `<code>${code.trim()}</code>`
    );
    
    // Handle inline code
    return formattedText.replace(
      /`([^`]+)`/g,
      (match, code) => `<code>${code}</code>`
    );
  };

  const handleSendMessage = async () => {
    if (message.trim()) {
      const userMessage = message;
      setChatMessages(prev => [...prev, { 
        text: userMessage, 
        sender: 'user',
        timestamp: new Date().toISOString()
      }]);
      setMessage('');
      
      // Show loading state
      setChatMessages(prev => [...prev, {
        text: "Processing your request...",
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isLoading: true
      }]);

      try {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
        const endpoint = serviceType === 'lawTeller' ? '/api/legal/query' : '/api/scholarship/search';
        
        const response = await fetch(`${backendUrl}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: userMessage,
            query: userMessage,
            language: 'en'
          })
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Remove loading message and add actual response
        setChatMessages(prev => {
          const filtered = prev.filter(msg => !msg.isLoading);
          const responseText = data.response || data.answer || JSON.stringify(data);
          return [...filtered, {
            text: responseText,
            sender: 'assistant',
            timestamp: new Date().toISOString()
          }];
        });
      } catch (error) {
        console.error('Error sending message:', error);
        setChatMessages(prev => {
          const filtered = prev.filter(msg => !msg.isLoading);
          return [...filtered, {
            text: `Error: ${error.message}. Please check if the backend is running on ${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}`,
            sender: 'system',
            timestamp: new Date().toISOString()
          }];
        });
      }
    }
  };

  const handleVoiceAssistant = () => {
    if (!recognition) {
      setChatMessages(prev => [...prev, {
        text: "Voice recognition is not supported in your browser. Please type your message instead.",
        sender: 'system'
      }]);
      return;
    }

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      try {
        // Clear any existing voice-related system messages
        setChatMessages(prev => prev.filter(msg => 
          !(msg.sender === 'system' && (
            msg.text.includes('Voice input') || 
            msg.text.includes('Voice recognition')
          ))
        ));
        recognition.start();
      } catch (error) {
        console.error('Speech recognition error:', error);
        setIsListening(false);
        setChatMessages(prev => [...prev, {
          text: "Could not start voice recognition. Please try again.",
          sender: 'system'
        }]);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      <Box sx={{ 
        minHeight: '100vh',
        height: '100vh',
        background: 'linear-gradient(135deg, #0a1929 0%, #102a43 100%)',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        overflow: 'hidden',
      }}>
        <Box sx={{
          p: { xs: 2, md: 2.5 },
          background: 'linear-gradient(135deg, rgba(13, 71, 161, 0.95), rgba(21, 101, 192, 0.95))',
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          position: 'sticky',
          top: 0,
          zIndex: 1000,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
        }}>
          <IconButton 
            onClick={() => navigate('/')}
            sx={{
              color: 'white',
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(5px)',
              transition: 'all 0.3s ease',
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.2)',
                transform: 'scale(1.1)',
              },
            }}
          >
            <ArrowBackIcon />
          </IconButton>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                width: 40,
                height: 40,
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #2196f3, #1565c0)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 20px rgba(33, 150, 243, 0.3)',
              }}
            >
              <ForumIcon sx={{ color: 'white', fontSize: 24 }} />
            </Box>
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'white', 
                fontWeight: '600',
                fontSize: { xs: '1.2rem', md: '1.3rem' },
                textShadow: '0 2px 4px rgba(0,0,0,0.2)',
              }}
            >
              {serviceType === 'lawTeller' ? 'Local Law Teller' : 'Scholarship Checker'}
            </Typography>
          </Box>
        </Box>

        <Box sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          height: 'calc(100vh - 72px)',
          position: 'relative',
          overflow: 'hidden',
        }}>
          <Box sx={{
            flex: 1,
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            px: { xs: 2, md: 3 },
            pt: { xs: 2, md: 3 },
            pb: 0,
            '&::-webkit-scrollbar': {
              width: '6px',
            },
            '&::-webkit-scrollbar-track': {
              background: 'transparent',
            },
            '&::-webkit-scrollbar-thumb': {
              background: 'rgba(255, 255, 255, 0.2)',
              borderRadius: '3px',
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.3)',
              },
            },
          }}>
            {chatMessages.length === 0 ? (
              <Box sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: 'calc(100vh - 180px)',
                gap: 3,
                opacity: 0.7,
              }}>
                <Box
                  sx={{
                    width: 80,
                    height: 80,
                    borderRadius: '24px',
                    background: 'linear-gradient(135deg, rgba(33, 150, 243, 0.2), rgba(33, 150, 243, 0.1))',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  <ForumIcon sx={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: 40 }} />
                </Box>
                <Typography
                  variant="h6"
                  sx={{
                    color: 'rgba(255, 255, 255, 0.7)',
                    textAlign: 'center',
                    maxWidth: '400px',
                    lineHeight: 1.6,
                  }}
                >
                  Start a conversation about {serviceType === 'lawTeller' ? 'legal matters' : 'scholarships'}
                </Typography>
              </Box>
            ) : (
              <Box sx={{ flexGrow: 1 }}>
                {chatMessages.map((msg, index) => (
                  <Box
                    key={index}
                    sx={{
                      width: '100%',
                      mb: 2,
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                      opacity: 0,
                      transform: 'translateY(20px)',
                      animation: 'fadeInUp 0.3s forwards',
                      animationDelay: `${index * 0.1}s`,
                      '@keyframes fadeInUp': {
                        '0%': {
                          opacity: 0,
                          transform: 'translateY(20px)',
                        },
                        '100%': {
                          opacity: 1,
                          transform: 'translateY(0)',
                        },
                      },
                    }}
                  >
                    <Box
                      sx={{
                        display: 'flex',
                        gap: 1.5,
                        alignItems: 'flex-start',
                        maxWidth: '80%',
                        flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
                      }}
                    >
                      <Box
                        sx={{
                          width: 36,
                          height: 36,
                          borderRadius: '12px',
                          background: msg.sender === 'user' 
                            ? 'linear-gradient(135deg, rgba(33, 150, 243, 0.9), rgba(21, 101, 192, 0.9))'
                            : 'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04))',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0,
                          boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
                        }}
                      >
                        <Typography sx={{ 
                          color: 'white', 
                          fontSize: '1rem', 
                          fontWeight: '600',
                          textShadow: '0 1px 2px rgba(0,0,0,0.2)',
                        }}>
                          {msg.sender === 'user' ? 'U' : 'A'}
                        </Typography>
                      </Box>
                      <Box
                        sx={{
                          background: msg.sender === 'user' 
                            ? 'linear-gradient(135deg, rgba(33, 150, 243, 0.9), rgba(21, 101, 192, 0.9))'
                            : 'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04))',
                          padding: '16px 20px',
                          borderRadius: msg.sender === 'user'
                            ? '20px 4px 20px 20px'
                            : '4px 20px 20px 20px',
                          position: 'relative',
                          boxShadow: msg.sender === 'user'
                            ? '0 8px 16px rgba(0, 0, 0, 0.15)'
                            : '0 4px 12px rgba(0, 0, 0, 0.1)',
                          maxWidth: '100%',
                          backdropFilter: 'blur(10px)',
                          border: msg.sender === 'user'
                            ? 'none'
                            : '1px solid rgba(255, 255, 255, 0.05)',
                          '&::before': {
                            content: '""',
                            position: 'absolute',
                            top: 0,
                            [msg.sender === 'user' ? 'right' : 'left']: -8,
                            width: 20,
                            height: 20,
                            background: msg.sender === 'user'
                              ? 'linear-gradient(135deg, rgba(33, 150, 243, 0.9), rgba(21, 101, 192, 0.9))'
                              : 'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04))',
                            clipPath: msg.sender === 'user'
                              ? 'polygon(0 0, 100% 0, 100% 100%)'
                              : 'polygon(0 0, 100% 0, 0 100%)',
                          },
                        }}
                      >
                        <Typography 
                          sx={{ 
                            color: 'white',
                            fontSize: { xs: '0.95rem', md: '1rem' },
                            lineHeight: 1.7,
                            letterSpacing: '0.2px',
                            wordBreak: 'break-word',
                            fontFamily: 'source-code-pro, Menlo, Monaco, Consolas, "Courier New", monospace',
                            whiteSpace: 'pre-wrap',
                            '& code': {
                              background: 'rgba(255, 255, 255, 0.1)',
                              padding: '2px 4px',
                              borderRadius: '4px',
                              fontFamily: 'inherit',
                              display: 'block',
                              margin: '8px 0',
                            },
                          }}
                          dangerouslySetInnerHTML={{ __html: formatMessage(msg.text) }}
                        />
                      </Box>
                    </Box>
                  </Box>
                ))}
              </Box>
            )}
          </Box>

          <Box sx={{
            position: 'sticky',
            bottom: 0,
            left: 0,
            right: 0,
            pt: 2,
            pb: { xs: 2, md: 2 },
            px: { xs: 2, md: 3 },
            background: 'linear-gradient(to top, #0a1929 95%, transparent)',
            zIndex: 10,
          }}>
            <Box sx={{
              maxWidth: '800px',
              margin: '0 auto',
              width: '100%',
            }}>
              <Paper
                elevation={0}
                sx={{
                  display: 'flex',
                  gap: { xs: 1, md: 1.5 },
                  alignItems: 'flex-end',
                  p: '12px 16px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  borderRadius: '16px',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                  backdropFilter: 'blur(10px)',
                  transition: 'all 0.3s ease',
                  '&:focus-within': {
                    boxShadow: '0 8px 32px rgba(33, 150, 243, 0.1)',
                    border: '1px solid rgba(33, 150, 243, 0.15)',
                    background: 'rgba(255, 255, 255, 0.03)',
                  },
                }}
              >
                <TextField
                  fullWidth
                  multiline
                  maxRows={4}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={`Ask anything about ${serviceType === 'lawTeller' ? 'legal matters' : 'scholarships'}...`}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      color: 'white',
                      backgroundColor: 'transparent',
                      '& fieldset': {
                        border: 'none',
                      },
                    },
                    '& .MuiInputBase-input': {
                      fontSize: { xs: '0.95rem', md: '1rem' },
                      padding: '4px 8px',
                      lineHeight: 1.7,
                      letterSpacing: '0.2px',
                      fontFamily: 'source-code-pro, Menlo, Monaco, Consolas, "Courier New", monospace',
                    },
                    '& .MuiInputBase-input::placeholder': {
                      color: 'rgba(255, 255, 255, 0.5)',
                      opacity: 1,
                    },
                  }}
                />
                
                <Tooltip title="Voice Assistant">
                  <IconButton 
                    onClick={handleVoiceAssistant}
                    size="small"
                    sx={{
                      color: 'white',
                      backgroundColor: isListening 
                        ? 'rgba(239, 83, 80, 0.2)'
                        : 'rgba(255, 255, 255, 0.1)',
                      padding: '10px',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: isListening 
                          ? 'rgba(239, 83, 80, 0.3)'
                          : 'rgba(255, 255, 255, 0.2)',
                        transform: 'scale(1.1)',
                      },
                    }}
                  >
                    {isListening ? <MicOffIcon /> : <MicIcon />}
                  </IconButton>
                </Tooltip>

                <Tooltip title="Send Message">
                  <IconButton 
                    onClick={handleSendMessage}
                    size="small"
                    sx={{
                      color: 'white',
                      backgroundColor: 'rgba(33, 150, 243, 0.2)',
                      padding: '10px',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(33, 150, 243, 0.3)',
                        transform: 'scale(1.1)',
                      },
                    }}
                  >
                    <SendIcon />
                  </IconButton>
                </Tooltip>
              </Paper>
            </Box>
          </Box>
        </Box>
      </Box>
      <RelatedContent serviceType={serviceType} />
    </>
  );
};

export default ChatInterface; 