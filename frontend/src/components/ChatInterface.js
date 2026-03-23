import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Paper,
  Typography,
  Tooltip,
  Chip,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ForumIcon from '@mui/icons-material/Forum';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import TranslateIcon from '@mui/icons-material/Translate';
import DownloadIcon from '@mui/icons-material/Download';
import { useNavigate } from 'react-router-dom';
import RelatedContent from './RelatedContent';

// Helper function to get law category icon
const getLawIcon = (lawText) => {
  const text = (lawText || '').toLowerCase();
  if (text.includes('theft') || text.includes('robbery') || text.includes('378')) return '🔓';
  if (text.includes('assault') || text.includes('323') || text.includes('325')) return '👊';
  if (text.includes('arms') || text.includes('gun') || text.includes('weapon')) return '🔫';
  if (text.includes('drug') || text.includes('ndps') || text.includes('narcotic')) return '💊';
  if (text.includes('kidnap') || text.includes('abduct') || text.includes('363')) return '🚨';
  if (text.includes('motor') || text.includes('vehicle') || text.includes('184')) return '🚗';
  if (text.includes('domestic') || text.includes('498a') || text.includes('dowry')) return '🏠';
  if (text.includes('cyber') || text.includes('it act') || text.includes('66')) return '💻';
  if (text.includes('fraud') || text.includes('cheat') || text.includes('420')) return '🤝';
  if (text.includes('consumer') || text.includes('cpa') || text.includes('rera')) return '🛒';
  if (text.includes('rape') || text.includes('pocso') || text.includes('375')) return '⚖️';
  if (text.includes('murder') || text.includes('homicide') || text.includes('302')) return '🔴';
  if (text.includes('out of scope')) return '⚠️';
  return '⚖️'; // Default legal icon
};

// Helper function to get risk color
const getRiskColor = (riskLevel) => {
  const level = (riskLevel || '').toLowerCase();
  if (level.includes('high')) return '#ff4444';
  if (level.includes('medium')) return '#ff9900';
  if (level.includes('low')) return '#00cc44';
  return '#888888'; // Unknown
};

// Typing indicator component
const TypingIndicator = ({ text = '⚖️ Analyzing your legal query' }) => (
  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, p: 2 }}>
    <Typography variant="caption" sx={{ color: '#4fc3f7', fontWeight: 500 }}>
      {text}
    </Typography>
    <Box sx={{ display: 'flex', gap: 0.5 }}>
      {[0, 1, 2].map(i => (
        <Box
          key={i}
          sx={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: '#4fc3f7',
            animation: 'bounce 1s infinite',
            animationDelay: `${i * 0.2}s`,
            '@keyframes bounce': {
              '0%, 100%': { transform: 'translateY(0)' },
              '50%': { transform: 'translateY(-8px)' },
            },
          }}
        />
      ))}
    </Box>
  </Box>
);

const ChatInterface = ({ serviceType }) => {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [recognition, setRecognition] = useState(null);
  const [language, setLanguage] = useState('en'); // 'en' or 'hi'
  const navigate = useNavigate();

  // Translation object for UI labels
  const translations = {
    en: {
      title: serviceType === 'lawTeller' ? 'Local Law Teller' : 'Scholarship Checker',
      placeholder: serviceType === 'lawTeller' 
        ? 'Describe your legal situation...' 
        : 'Search for scholarships...',
      send: 'Send Message',
      voice: 'Voice Input',
      stopRecording: 'Stop Recording',
      clearHistory: 'Clear Chat History',
      analyzing: '⚖️ Analyzing your legal query',
    },
    hi: {
      title: serviceType === 'lawTeller' ? 'स्थानीय कानून सलाहकार' : 'छात्रवृत्ति जांचकर्ता',
      placeholder: serviceType === 'lawTeller'
        ? 'अपनी कानूनी स्थिति का वर्णन करें...'
        : 'छात्रवृत्ति खोजें...',
      send: 'संदेश भेजें',
      voice: 'ध्वनि इनपुट',
      stopRecording: 'रिकॉर्डिंग बंद करें',
      clearHistory: 'चैट इतिहास साफ़ करें',
      analyzing: '⚖️ आपके कानूनी प्रश्न का विश्लेषण किया जा रहा है',
    }
  };

  const t = translations[language];

  // Query suggestions based on service type
  const querySuggestions = serviceType === 'lawTeller' ? [
    "Someone hacked my bank account",
    "My neighbor stole my bicycle",
    "I was assaulted by my landlord",
    "Insurance company rejected my claim",
    "Contractor took advance and disappeared",
    "My employer didn't pay salary for 3 months",
    "Property dispute with neighbor",
    "Illegal gun possession case"
  ] : [
    "Merit-based scholarships for engineering",
    "Scholarships for SC/ST students",
    "Financial aid for medical students",
    "Overseas education scholarships"
  ];

  useEffect(() => {
    let recognitionInstance = null;
    
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = language === 'hi' ? 'hi-IN' : 'en-US';

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
          !(msg.sender === 'system' && (
            msg.text.includes('Voice recognition error') ||
            msg.text.includes('Microphone') ||
            msg.text.includes('voice input')
          ))
        ));

        // Add appropriate error message based on the error type
        let errorMessage = "";
        
        if (event.error === 'not-allowed') {
          errorMessage = "🎤 Microphone access denied. Please enable microphone permissions in your browser settings and try again.";
        } else if (event.error === 'network') {
          errorMessage = "🌐 Voice input requires HTTPS connection. On HTTP (localhost), please type your message instead. Voice input will work on deployed HTTPS sites.";
        } else if (event.error === 'no-speech') {
          // Don't show no-speech error in continuous mode
          return;
        } else if (event.error === 'audio-capture') {
          errorMessage = "🎤 No microphone detected. Please connect a microphone and try again, or type your message.";
        } else if (event.error === 'aborted') {
          // User intentionally stopped - don't show error
          return;
        } else {
          errorMessage = `⚠️ Voice recognition error (${event.error}). Please try again or type your message.`;
        }

        if (errorMessage) {
          setChatMessages(prev => [...prev, {
            text: errorMessage,
            sender: 'system',
            timestamp: new Date().toISOString()
          }]);
        }
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
  }, [isListening, language]); // Add language to the dependency array

  // Load chat history from localStorage on mount
  useEffect(() => {
    const storageKey = `chatHistory_${serviceType}`;
    const savedHistory = localStorage.getItem(storageKey);
    if (savedHistory) {
      try {
        const parsedHistory = JSON.parse(savedHistory);
        setChatMessages(parsedHistory);
      } catch (error) {
        console.error('Error loading chat history:', error);
      }
    }
  }, [serviceType]);

  // Save chat messages to localStorage whenever they change
  useEffect(() => {
    if (chatMessages.length > 0) {
      const storageKey = `chatHistory_${serviceType}`;
      // Filter out loading messages before saving
      const messagestoSave = chatMessages.filter(msg => !msg.isLoading);
      localStorage.setItem(storageKey, JSON.stringify(messagestoSave));
    }
  }, [chatMessages, serviceType]);

  // Clear chat history
  const handleClearHistory = () => {
    setChatMessages([]);
    const storageKey = `chatHistory_${serviceType}`;
    localStorage.removeItem(storageKey);
  };

  // Download response as PDF (using text format in a downloadable file)
  const handleDownloadPDF = (msg) => {
    let content = '';
    
    if (msg.structured_data) {
      const data = msg.structured_data;
      content = `LEGAL ANALYSIS REPORT
==================

Query: ${msg.query || 'N/A'}

Applicable Law: ${data.applicable_law || 'N/A'}

Legal Position:
${data.legal_position || 'N/A'}

Risk Level: ${data.risk_level || 'N/A'}

Next Steps:
${data.next_steps || 'N/A'}

${data.disclaimer ? `\nDisclaimer:\n${data.disclaimer}` : ''}

Generated: ${new Date(msg.timestamp).toLocaleString()}
`;
    } else {
      content = `LEGAL QUERY RESPONSE
===================

${msg.text}

Generated: ${new Date(msg.timestamp).toLocaleString()}
`;
    }

    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `legal-response-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  const formatMessage = (text) => {
    if (!text) return '';
    if (typeof text !== 'string') {
      text = JSON.stringify(text, null, 2);
    }
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
        let endpoint = '';
        let body = {};
        if (serviceType === 'lawTeller') {
          endpoint = '/api/predict';
          body = { 
            query: language === 'hi' 
              ? `${userMessage} (Please provide response in Hindi)` 
              : userMessage 
          };
        } else {
          endpoint = '/api/scholarship/search';
          body = { query: userMessage, language: language };
        }

        console.log('Sending request to:', `${backendUrl}${endpoint}`);
        console.log('Request body:', body);

        const response = await fetch(`${backendUrl}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
          timeout: 30000 // 30 second timeout
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
          const errorText = await response.text();
          console.error('API error response:', errorText);
          throw new Error(`API error: ${response.status} ${response.statusText} - ${errorText}`);
        }

        const data = await response.json();
        console.log('API Response data:', data);
        
        // Remove loading message and add actual response
        setChatMessages(prev => {
          const filtered = prev.filter(msg => !msg.isLoading);
          
          // Handle different response formats from backend
          let responseData = data.response || data;
          let responseText = '';
          let parsedStructured = null;
          
          // Extract structured data from various possible locations
          if (responseData.structured_data) {
            parsedStructured = responseData.structured_data;
          } else if (responseData.applicable_law) {
            parsedStructured = responseData;
          } else if (data.structured_data) {
            parsedStructured = data.structured_data;
          } else if (data.applicable_law) {
            parsedStructured = data;
          }
          
          // Extract text from various possible locations
          if (parsedStructured) {
            responseText = (
              parsedStructured.legal_position || 
              parsedStructured.prediction || 
              parsedStructured.applicable_law || 
              ''
            );
          } else {
            responseText = (
              responseData.prediction || 
              responseData.legal_position ||
              responseData.text ||
              responseData.answer ||
              (typeof responseData === 'string' ? responseData : JSON.stringify(responseData))
            );
          }
          
          console.log('Parsed structured data:', parsedStructured);
          console.log('Response text:', responseText);

          // Create the new message
          const newMessage = {
            text: responseText,
            sender: 'assistant',
            timestamp: new Date().toISOString(),
            query: userMessage
          };

          if (parsedStructured) {
            newMessage.structured_data = parsedStructured;
          }
          
          // Add confidence if available
          const confidence = (
            data.confidence || 
            data.response?.confidence || 
            parsedStructured?.confidence
          );
          if (confidence !== undefined) {
            newMessage.confidence = confidence;
          }

          return [...filtered, newMessage];
        });
      } catch (error) {
        console.error('Error sending message:', error);
        console.error('Error details:', {
          message: error.message,
          stack: error.stack
        });
        
        setChatMessages(prev => {
          const filtered = prev.filter(msg => !msg.isLoading);
          return [...filtered, {
            text: `Error: ${error.message}. Please check if the backend is running on ${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}`,
            sender: 'system',
            timestamp: new Date().toISOString(),
            isError: true
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
        margin: 0,
        padding: 0,
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a1929 0%, #102a43 100%)',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        overflowX: 'hidden',
      }}>
        <Box sx={{
          p: { xs: 2, md: 2.5 },
          background: 'linear-gradient(135deg, rgba(13, 71, 161, 0.95), rgba(21, 101, 192, 0.95))',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 2,
          position: 'sticky',
          top: 0,
          zIndex: 1000,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
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
                {t.title}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title={language === 'en' ? 'Switch to Hindi' : 'Switch to English'}>
              <IconButton
                onClick={() => setLanguage(lang => lang === 'en' ? 'hi' : 'en')}
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
                <TranslateIcon />
                <Typography sx={{ ml: 0.5, fontSize: '0.75rem', fontWeight: 'bold' }}>
                  {language === 'en' ? 'HI' : 'EN'}
                </Typography>
              </IconButton>
            </Tooltip>
            {chatMessages.length > 0 && (
              <Tooltip title={t.clearHistory}>
                <IconButton
                  onClick={handleClearHistory}
                  sx={{
                    color: 'white',
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(5px)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      background: 'rgba(255, 100, 100, 0.3)',
                      transform: 'scale(1.1)',
                    },
                  }}
                >
                  <DeleteSweepIcon />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        </Box>

        <Box sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          height: 'calc(100vh - 72px)',
          position: 'relative',
overflowX: 'hidden',
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
                
                {/* Query Suggestions */}
                <Box sx={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  gap: 2, 
                  alignItems: 'center',
                  maxWidth: { xs: '90%', md: '600px' }
                }}>
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.5)',
                      textTransform: 'uppercase',
                      letterSpacing: 1,
                      fontWeight: 600
                    }}
                  >
                    Try these examples:
                  </Typography>
                  <Box sx={{ 
                    display: 'flex', 
                    flexWrap: 'wrap', 
                    gap: 1, 
                    justifyContent: 'center' 
                  }}>
                    {querySuggestions.map((suggestion, idx) => (
                      <Chip
                        key={idx}
                        label={suggestion}
                        onClick={() => {
                          setMessage(suggestion);
                          setTimeout(() => handleSendMessage(), 100);
                        }}
                        sx={{
                          background: 'rgba(33, 150, 243, 0.15)',
                          color: '#90caf9',
                          border: '1px solid rgba(33, 150, 243, 0.3)',
                          fontSize: '0.85rem',
                          cursor: 'pointer',
                          transition: 'all 0.3s ease',
                          '&:hover': {
                            background: 'rgba(33, 150, 243, 0.25)',
                            borderColor: 'rgba(33, 150, 243, 0.5)',
                            transform: 'translateY(-2px)',
                            boxShadow: '0 4px 12px rgba(33, 150, 243, 0.2)',
                          },
                        }}
                      />
                    ))}
                  </Box>
                </Box>
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
                            : 'rgba(255,255,255,0.05)',
                          padding: '16px 20px',
                          borderRadius: msg.sender === 'user'
                            ? '20px 4px 20px 20px'
                            : '4px 20px 20px 20px',
                          position: 'relative',
                          boxShadow: msg.sender === 'user'
                            ? '0 8px 16px rgba(0, 0, 0, 0.15)'
                            : 'none',
                          maxWidth: '100%',
                          backdropFilter: 'blur(10px)',
                          border: 'none',
                          outline: 'none',
                          '&::before': {
                            content: '""',
                            position: 'absolute',
                            top: 0,
                            [msg.sender === 'user' ? 'right' : 'left']: -8,
                            width: 20,
                            height: 20,
                            background: msg.sender === 'user'
                              ? 'linear-gradient(135deg, rgba(33, 150, 243, 0.9), rgba(21, 101, 192, 0.9))'
                              : 'rgba(255,255,255,0.05)',
                            clipPath: msg.sender === 'user'
                              ? 'polygon(0 0, 100% 0, 100% 100%)'
                              : 'polygon(0 0, 100% 0, 0 100%)',
                          },
                        }}
                      >
                        {/* Structured Legal Response Rendering */}
                        {msg.sender === 'assistant' && msg.structured_data ? (
                          <>
                            {/* Special handling for Out of Scope */}
                            {msg.structured_data.applicable_law === 'Out of Scope' ? (
                              <Box sx={{
                                background: 'rgba(255, 165, 0, 0.1)',
                                border: '1px solid rgba(255, 165, 0, 0.3)',
                                borderRadius: '12px',
                                p: 2,
                                display: 'flex',
                                flexDirection: 'column',
                                gap: 1.5
                              }}>
                                <Typography sx={{ 
                                  color: '#ffb74d', 
                                  fontWeight: 'bold',
                                  fontSize: '1rem',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: 1
                                }}>
                                  ⚠️ Out of Legal Scope
                                </Typography>
                                <Typography sx={{ color: 'rgba(255, 255, 255, 0.9)', lineHeight: 1.6 }}>
                                  {msg.structured_data.legal_position}
                                </Typography>
                                <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '0.875rem' }}>
                                  📞 Legal Aid Helpline: <strong style={{ color: '#fff' }}>15100</strong>
                                </Typography>
                              </Box>
                            ) : (
                              <Box sx={{
                                background: 'linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02))',
                                borderLeft: `4px solid ${getRiskColor(msg.structured_data.risk_level)}`,
                                borderRadius: '12px',
                                padding: { xs: '12px', md: '20px' },
                                marginBottom: 0,
                                backdropFilter: 'blur(10px)',
                                display: 'flex',
                                flexDirection: 'column',
                                gap: 1.5
                              }}>
                                {/* Law Category Icon + Applicable Law */}
                                <Box>
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                                    <Typography sx={{ fontSize: '1.5rem' }}>
                                      {getLawIcon(msg.structured_data.applicable_law)}
                                    </Typography>
                                    <Typography variant="overline" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 'bold' }}>
                                      Applicable Law + Section
                                    </Typography>
                                  </Box>
                                  <Typography variant="body1" sx={{ 
                                    color: '#90caf9', 
                                    fontWeight: 700,
                                    fontSize: { xs: '13px', md: '15px' },
                                    background: 'rgba(144, 202, 249, 0.1)',
                                    padding: '8px 12px',
                                    borderRadius: '8px',
                                    border: '1px solid rgba(144, 202, 249, 0.2)'
                                  }}>
                                    ⚖️ {msg.structured_data.applicable_law}
                                  </Typography>
                                </Box>

                                {/* Separator */}
                                <Box sx={{ height: '1px', background: 'rgba(255,255,255,0.08)', my: 0.5 }} />

                                {/* Legal Position */}
                                <Box>
                                  <Typography variant="overline" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 'bold' }}>
                                    Legal Position
                                  </Typography>
                                  <Typography variant="body2" sx={{ 
                                    color: 'white', 
                                    lineHeight: 1.6,
                                    fontSize: { xs: '13px', md: '15px' }
                                  }}>
                                    {msg.structured_data.legal_position}
                                  </Typography>
                                </Box>

                                {/* Separator */}
                                <Box sx={{ height: '1px', background: 'rgba(255,255,255,0.08)', my: 0.5 }} />

                                {/* Outcome & Risk */}
                                <Box sx={{ 
                                  display: 'flex', 
                                  gap: 2, 
                                  alignItems: { xs: 'flex-start', md: 'center' },
                                  flexDirection: { xs: 'column', md: 'row' },
                                  mt: 1 
                                }}>
                                  <Box sx={{ flex: 1 }}>
                                    <Typography variant="overline" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 'bold' }}>
                                      Outcome
                                    </Typography>
                                    <Typography variant="body2" sx={{ 
                                      color: 'white',
                                      fontSize: { xs: '13px', md: '14px' }
                                    }}>
                                      {msg.structured_data.predicted_outcome}
                                    </Typography>
                                  </Box>
                                  <Box>
                                    <Typography variant="overline" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 'bold', display: 'block', mb: 0.5 }}>
                                      Risk Level
                                    </Typography>
                                    <Box sx={{ 
                                      px: 1.5, 
                                      py: 0.5, 
                                      borderRadius: '12px',
                                      fontSize: '0.75rem',
                                      fontWeight: 'bold',
                                      textTransform: 'uppercase',
                                      textAlign: 'center',
                                      minWidth: '80px',
                                      backgroundColor: getRiskColor(msg.structured_data.risk_level) + '33',
                                      color: getRiskColor(msg.structured_data.risk_level),
                                      border: `2px solid ${getRiskColor(msg.structured_data.risk_level)}`,
                                      boxShadow: `0 0 12px ${getRiskColor(msg.structured_data.risk_level)}44`
                                    }}>
                                      {msg.structured_data.risk_level}
                                    </Box>
                                  </Box>
                                </Box>

                                {/* Separator */}
                                <Box sx={{ height: '1px', background: 'rgba(255,255,255,0.08)', my: 0.5 }} />

                                {/* Next Steps */}
                                {msg.structured_data.next_steps && msg.structured_data.next_steps.length > 0 && (
                                  <Box sx={{ mt: 1 }}>
                                    <Typography variant="overline" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 'bold' }}>
                                      Next Steps
                                    </Typography>
                                    <Box component="ul" sx={{ m: 0, p: 0, listStyle: 'none' }}>
                                      {msg.structured_data.next_steps.map((step, i) => (
                                        <Box component="li" key={i} sx={{ 
                                          display: 'flex', 
                                          gap: 1, 
                                          mb: 0.5, 
                                          fontSize: { xs: '0.8rem', md: '0.85rem' },
                                          color: 'rgba(255,255,255,0.8)' 
                                        }}>
                                          <Typography sx={{ color: '#2196f3', fontWeight: 'bold' }}>{i + 1}.</Typography>
                                          <Typography variant="body2">{step}</Typography>
                                        </Box>
                                      ))}
                                    </Box>
                                  </Box>
                                )}

                                {/* Helpline */}
                                {msg.structured_data.helpline && (
                                  <Box sx={{ mt: 1, p: 1, borderRadius: '8px', backgroundColor: 'rgba(255,255,255,0.05)' }}>
                                    <Typography sx={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.6)' }}>
                                      📞 Helpline: <strong style={{ color: '#fff' }}>{msg.structured_data.helpline}</strong>
                                    </Typography>
                                  </Box>
                                )}

                                {/* Disclaimer */}
                                {msg.structured_data.disclaimer && (
                                  <Typography sx={{ 
                                    mt: 1, 
                                    fontSize: '0.65rem', 
                                    color: 'rgba(255,255,255,0.4)', 
                                    fontStyle: 'italic',
                                    textAlign: 'center',
                                    borderTop: '1px solid rgba(255,255,255,0.05)',
                                    pt: 1
                                  }}>
                                    {msg.structured_data.disclaimer}
                                  </Typography>
                                )}
                              </Box>
                            )}
                          </>
                        ) : serviceType === 'scholarship' && msg.sender === 'assistant' && !msg.isLoading ? (
                          <>
                            {/* Scholarship Cards Display */}
                            {(() => {
                              console.log('Scholarship render check:', {
                                serviceType,
                                sender: msg.sender,
                                isLoading: msg.isLoading,
                                msgText: msg.text?.substring(0, 100)
                              });
                              try {
                                // Try to parse the response as JSON
                                const scholarshipData = typeof msg.text === 'string' ? JSON.parse(msg.text) : msg.text;
                                const scholarships = scholarshipData.scholarships || [];
                                console.log('Parsed scholarships:', scholarships.length);
                                
                                if (scholarships.length > 0) {
                                  return (
                                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                      {scholarships.map((scholarship, index) => {
                                        const isActive = scholarship.status === 'Active';
                                        const borderColor = isActive ? '#4caf50' : '#f44336';
                                        
                                        return (
                                          <Box
                                            key={index}
                                            sx={{
                                              background: 'rgba(255,255,255,0.05)',
                                              borderRadius: '12px',
                                              borderLeft: `4px solid ${borderColor}`,
                                              padding: 2,
                                              transition: 'all 0.3s ease',
                                              '&:hover': {
                                                background: 'rgba(255,255,255,0.08)',
                                                transform: 'translateX(4px)',
                                              }
                                            }}
                                          >
                                            {/* Scholarship Name */}
                                            <Typography sx={{ 
                                              fontSize: '1.1rem', 
                                              fontWeight: 600, 
                                              color: 'white',
                                              mb: 1,
                                              display: 'flex',
                                              alignItems: 'center',
                                              gap: 1
                                            }}>
                                              🎓 {scholarship.name}
                                            </Typography>
                                            
                                            {/* Description */}
                                            <Typography sx={{ 
                                              fontSize: '0.9rem', 
                                              color: 'rgba(255,255,255,0.7)',
                                              mb: 1.5,
                                              lineHeight: 1.6
                                            }}>
                                              {scholarship.description}
                                            </Typography>
                                            
                                            {/* Amount and Deadline Row */}
                                            <Box sx={{ display: 'flex', gap: 3, mb: 1.5, flexWrap: 'wrap' }}>
                                              <Typography sx={{ 
                                                fontSize: '0.85rem', 
                                                color: 'rgba(255,255,255,0.8)',
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: 0.5
                                              }}>
                                                💰 <strong>Amount:</strong> {scholarship.amount}
                                              </Typography>
                                              
                                              <Typography sx={{ 
                                                fontSize: '0.85rem', 
                                                color: 'rgba(255,255,255,0.8)',
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: 0.5
                                              }}>
                                                📅 <strong>Deadline:</strong> {scholarship.deadline}
                                              </Typography>
                                              
                                              <Typography sx={{ 
                                                fontSize: '0.85rem',
                                                fontWeight: 600,
                                                color: isActive ? '#4caf50' : '#f44336',
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: 0.5
                                              }}>
                                                {isActive ? '✓' : '✗'} {scholarship.status}
                                              </Typography>
                                            </Box>
                                            
                                            {/* Eligibility */}
                                            {scholarship.eligibility && scholarship.eligibility.length > 0 && (
                                              <Box sx={{ mb: 1.5 }}>
                                                <Typography sx={{ 
                                                  fontSize: '0.85rem', 
                                                  color: 'rgba(255,255,255,0.9)',
                                                  fontWeight: 600,
                                                  mb: 0.5
                                                }}>
                                                  ✅ Eligibility:
                                                </Typography>
                                                <Box sx={{ pl: 2 }}>
                                                  {(Array.isArray(scholarship.eligibility) 
                                                    ? scholarship.eligibility 
                                                    : scholarship.eligibility.split(';')
                                                  ).map((item, i) => (
                                                    <Typography key={i} sx={{ 
                                                      fontSize: '0.8rem', 
                                                      color: 'rgba(255,255,255,0.7)',
                                                      mb: 0.3
                                                    }}>
                                                      • {typeof item === 'string' ? item.trim() : item}
                                                    </Typography>
                                                  ))}
                                                </Box>
                                              </Box>
                                            )}
                                            
                                            {/* Apply Button */}
                                            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
                                              <Box
                                                component="a"
                                                href={scholarship.application_link}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                sx={{
                                                  display: 'inline-flex',
                                                  alignItems: 'center',
                                                  gap: 0.5,
                                                  padding: '8px 16px',
                                                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                                  color: 'white',
                                                  fontSize: '0.85rem',
                                                  fontWeight: 600,
                                                  borderRadius: '8px',
                                                  textDecoration: 'none',
                                                  transition: 'all 0.3s ease',
                                                  '&:hover': {
                                                    transform: 'translateY(-2px)',
                                                    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
                                                  }
                                                }}
                                              >
                                                Apply Now →
                                              </Box>
                                            </Box>
                                          </Box>
                                        );
                                      })}
                                    </Box>
                                  );
                                } else {
                                  return (
                                    <Typography sx={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.9rem' }}>
                                      No scholarships found matching your query.
                                    </Typography>
                                  );
                                }
                              } catch (e) {
                                // If JSON parsing fails, show the text as-is
                                console.error('Failed to parse scholarship response:', e);
                                return (
                                  <Typography 
                                    sx={{ 
                                      color: 'white',
                                      fontSize: { xs: '0.95rem', md: '1rem' },
                                      lineHeight: 1.7,
                                      letterSpacing: '0.2px',
                                      wordBreak: 'break-word',
                                      fontFamily: 'source-code-pro, Menlo, Monaco, Consolas, "Courier New", monospace',
                                      whiteSpace: 'pre-wrap',
                                    }}
                                    dangerouslySetInnerHTML={{ __html: formatMessage(msg.text) }}
                                  />
                                );
                              }
                            })()}
                          </>
                        ) : (
                          <>
                            {msg.isLoading ? (
                              <TypingIndicator text={t.analyzing} />
                            ) : (
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
                            )}
                          </>
                        )}
                        
                        {/* Status Footer */}
                        {msg.sender === 'assistant' && !msg.isLoading && (
                          <Box sx={{ mt: 2, pt: 1, borderTop: '1px solid rgba(255,255,255,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                              {msg.confidence !== undefined && (
                                <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.5)', display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <span style={{ 
                                    width: 6, 
                                    height: 6, 
                                    borderRadius: '50%', 
                                    backgroundColor: msg.confidence > 0.8 ? '#4caf50' : msg.confidence > 0.5 ? '#ff9800' : '#f44336' 
                                  }}></span>
                                  Confidence: {Math.round(msg.confidence * 100)}%
                                </Typography>
                              )}
                              <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>
                                Local Engine
                              </Typography>
                            </Box>
                            <Tooltip title="Download as TXT">
                              <IconButton
                                onClick={() => handleDownloadPDF(msg)}
                                size="small"
                                sx={{
                                  color: 'rgba(255,255,255,0.5)',
                                  padding: '4px',
                                  '&:hover': {
                                    color: '#4fc3f7',
                                    background: 'rgba(79, 195, 247, 0.1)',
                                  },
                                }}
                              >
                                <DownloadIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        )}
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
                  placeholder={t.placeholder}
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
                
                <Tooltip title={isListening ? t.stopRecording : t.voice}>
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
                      animation: isListening ? 'pulse 1.5s infinite' : 'none',
                      '@keyframes pulse': {
                        '0%, 100%': { 
                          boxShadow: '0 0 0 0 rgba(239, 83, 80, 0.7)',
                        },
                        '50%': { 
                          boxShadow: '0 0 0 10px rgba(239, 83, 80, 0)',
                        },
                      },
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

                <Tooltip title={t.send}>
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