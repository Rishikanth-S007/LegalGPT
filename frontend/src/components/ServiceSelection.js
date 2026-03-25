import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  List,
  ListItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Divider,
  Snackbar,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Avatar,
} from '@mui/material';
import GavelIcon from '@mui/icons-material/Gavel';
import SchoolIcon from '@mui/icons-material/School';
import GoogleIcon from '@mui/icons-material/Google';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CloseIcon from '@mui/icons-material/Close';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const ServiceSelection = () => {
  const navigate = useNavigate();
  const { isLoggedIn, login, loginWithGoogle, register, logout } = useAuth();
  const [language, setLanguage] = useState('en');
  
  const [openSignUpDialog, setOpenSignUpDialog] = useState(false);
  const [openLoginDialog, setOpenLoginDialog] = useState(false);
  const [openNotification, setOpenNotification] = useState(false);
  const [openError, setOpenError] = useState(false);
  const [selectedService, setSelectedService] = useState(null);
  const [signUpData, setSignUpData] = useState({
    email: '',
    password: '',
  });
  const [loginData, setLoginData] = useState({
    email: '',
    password: '',
  });
  const [expanded, setExpanded] = useState(false);

  const handleGoogleSignUp = () => {
    // TODO: Implement Google Sign Up
    console.log('Google Sign Up clicked');
    setOpenSignUpDialog(false);
  };

   const handleGoogleSuccess = async (credentialResponse) => {
     try {
       const result = await axios.post(
         `${process.env.REACT_APP_BACKEND_URL}/api/auth/google`,
         { credential: credentialResponse.credential }
       );
       const { access_token, user } = result.data;
       loginWithGoogle(access_token, user);
       setOpenLoginDialog(false);
       navigate('/');
     } catch (err) {
       console.error('Google login error:', err);
       alert('Google login failed. Try again.');
     }
   };

  const handleGoogleError = () => {
    console.error('Google login failed');
    alert('Google login failed');
  };

  const handleSignUp = async () => {
    const result = await register(signUpData.email, signUpData.password);
    if (result.success) {
      console.log('Sign Up successful');
      setOpenSignUpDialog(false);
      // Auto-login after signup
      await login(signUpData.email, signUpData.password);
    } else {
      alert(result.error);
    }
  };

  const handleLogin = async () => {
    const result = await login(loginData.email, loginData.password);
    if (result.success) {
      console.log('Login successful');
      setOpenLoginDialog(false);
      // No navigation needed, state will update UI
    } else {
      alert(result.error);
    }
  };

  const handleServiceSelection = (service, path) => {
    if (!isLoggedIn) {
      setOpenError(true);
      setOpenLoginDialog(true);
      return;
    }
    
    setSelectedService(service);
    setOpenNotification(true);
    setTimeout(() => {
      navigate(path);
    }, 2000);
  };

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const faqData = {
    en: [
      {
        question: "What is AI Lawyer?",
        answer: "AI Lawyer is a cutting-edge platform that transforms law market using artificial intelligence. It automates research, simplifies complex terms, and handles documents efficiently. Ideal for individuals seeking affordable consultation and for professionals and students aiming to streamline their work. It offers personalized customization, multi-platform access, and prioritizes privacy, making it a valuable tool in LegalTech market."
      },
      {
        question: "Who is your platform for?",
        answer: "Our platform serves a diverse range of users including legal professionals, students, businesses, and individuals seeking legal assistance. It's particularly useful for those who need quick access to legal information, document analysis, or scholarship opportunities."
      },
      {
        question: "What countries/languages does it works for?",
        answer: "Currently, our platform supports multiple languages including English and Hindi. We provide legal information and scholarship details for various countries, with a primary focus on Indian law and international scholarship opportunities."
      },
      {
        question: "How to start using AI Lawyer?",
        answer: "Getting started is simple: 1. Choose your service (Law Teller or Scholarship Checker), 2. Create an account or log in, 3. Start asking questions or searching for opportunities. Our AI will guide you through the process with clear, simple responses."
      },
      {
        question: "How to get \"Students & teachers\" discount?",
        answer: "Students and teachers can receive special discounts by verifying their academic status. Simply register with your institutional email address or provide valid academic credentials during signup to automatically qualify for the discount."
      },
      {
        question: "Can I receive a refund if I'm not satisfied?",
        answer: "Yes, we offer a satisfaction guarantee. If you're not satisfied with our services, you can request a refund within 30 days of your subscription. Contact our support team with your concerns, and we'll process your refund according to our refund policy."
      },
      {
        question: "Will AI replace lawyers?",
        answer: "No, AI will not replace lawyers. Instead, it serves as a powerful tool to augment legal professionals' capabilities. AI helps with routine tasks, research, and initial analysis, allowing lawyers to focus on complex decision-making, strategy, and client relationships that require human expertise and judgment."
      }
    ],
    hi: [
      {
        question: "AI लॉयर क्या है?",
        answer: "AI लॉयर एक अत्याधुनिक प्लेटफॉर्म है जो कृत्रिम बुद्धिमत्ता का उपयोग करके कानूनी क्षेत्र को बदल रहा है। यह रिसर्च को स्वचालित करता है, जटिल शब्दों को सरल बनाता है, और दस्तावेजों को कुशलतापूर्वक संभालता है। किफायती परामर्श चाहने वाले व्यक्तियों और अपने काम को सुव्यवस्थित करने के लिए पेशेवरों और छात्रों के लिए आदर्श है।"
      },
      {
        question: "आपका प्लेटफॉर्म किसके लिए है?",
        answer: "हमारा प्लेटफॉर्म कानूनी पेशेवरों, छात्रों, व्यवसायों और कानूनी सहायता चाहने वाले व्यक्तियों सहित विभिन्न उपयोगकर्ताओं की सेवा करता है। यह विशेष रूप से उन लोगों के लिए उपयोगी है जिन्हें कानूनी जानकारी, दस्तावेज विश्लेषण या छात्रवृत्ति के अवसरों तक त्वरित पहुंच की आवश्यकता है।"
      },
      {
        question: "यह किन देशों/भाषाओं के लिए काम करता है?",
        answer: "वर्तमान में, हमारा प्लेटफॉर्म अंग्रेजी और हिंदी सहित कई भाषाओं का समर्थन करता है। हम भारतीय कानून और अंतर्राष्ट्रीय छात्रवृत्ति के अवसरों पर विशेष ध्यान देने के साथ विभिन्न देशों के लिए कानूनी जानकारी और छात्रवृत्ति विवरण प्रदान करते हैं।"
      },
      {
        question: "AI लॉयर का उपयोग कैसे शुरू करें?",
        answer: "शुरू करना बहुत आसान है: 1. अपनी सेवा चुनें (लॉ टेलर या स्कॉलरशिप चेकर), 2. खाता बनाएं या लॉग इन करें, 3. प्रश्न पूछना या अवसर खोजना शुरू करें। हमारी AI स्पष्ट, सरल प्रतिक्रियाओं के साथ आपका मार्गदर्शन करेगी।"
      },
      {
        question: "\"छात्र और शिक्षक\" छूट कैसे प्राप्त करें?",
        answer: "छात्र और शिक्षक अपनी शैक्षणिक स्थिति की पुष्टि करके विशेष छूट प्राप्त कर सकते हैं। साइनअप के दौरान अपने संस्थागत ईमेल पते या वैध शैक्षणिक प्रमाणपत्र के साथ पंजीकरण करें और स्वचालित रूप से छूट के लिए पात्र बन जाएं।"
      },
      {
        question: "क्या मैं रिफंड प्राप्त कर सकता हूं यदि मैं संतुष्ट नहीं हूं?",
        answer: "हां, हम संतुष्टि की गारंटी देते हैं। यदि आप हमारी सेवाओं से संतुष्ट नहीं हैं, तो आप अपनी सदस्यता के 30 दिनों के भीतर रिफंड का अनुरोध कर सकते हैं। अपनी चिंताओं के साथ हमारी सहायता टीम से संपर्क करें, और हम हमारी रिफंड नीति के अनुसार आपका रिफंड प्रोसेस करेंगे।"
      },
      {
        question: "क्या AI वकीलों की जगह लेगी?",
        answer: "नहीं, AI वकीलों की जगह नहीं लेगी। इसके बजाय, यह कानूनी पेशेवरों की क्षमताओं को बढ़ाने के लिए एक शक्तिशाली उपकरण के रूप में काम करती है। AI नियमित कार्यों, अनुसंधान और प्रारंभिक विश्लेषण में मदद करती है, जिससे वकील जटिल निर्णय लेने, रणनीति और ग्राहक संबंधों पर ध्यान केंद्रित कर सकते हैं जिनके लिए मानवीय विशेषज्ञता और निर्णय की आवश्यकता होती है।"
      }
    ]
  };

  const serviceIntros = {
    lawTeller: {
      en: {
        title: 'LOCAL LAW\nTELLER',
        description: 'YOUR AI-POWERED LEGAL\nASSISTANT AVAILABLE 24/7',
        subtext: 'GET INSTANT ANSWERS TO YOUR LEGAL\nQUERIES IN SIMPLE LANGUAGE',
        features: [
          'Real-time access to local laws and regulations',
          'AI-powered legal document analysis',
          'Simplified explanations of complex legal terms',
          '24/7 availability for legal information',
          'Regular updates with latest legal changes',
          'Voice-enabled queries and responses'
        ]
      },
      hi: {
        title: 'लोकल लॉ\nटेलर',
        description: '24/7 उपलब्ध आपका\nएआई-संचालित कानूनी सहायक',
        subtext: 'सरल भाषा में अपने कानूनी प्रश्नों के\nतुरंत उत्तर प्राप्त करें',
        features: [
          'स्थानीय कानूनों और नियमों तक तत्काल पहुंच',
          'एआई-संचालित कानूनी दस्तावेज़ विश्लेषण',
          'जटिल कानूनी शब्दों की सरल व्याख्या',
          'कानूनी जानकारी के लिए 24/7 उपलब्धता',
          'नवीनतम कानूनी परिवर्तनों के साथ नियमित अपडेट',
          'आवाज-सक्षम प्रश्न और उत्तर'
        ]
      }
    },
    scholarship: {
      en: {
        title: 'SCHOLARSHIP\nCHECKER',
        description: 'FIND THE PERFECT\nSCHOLARSHIP OPPORTUNITIES',
        subtext: 'GET PERSONALIZED\nRECOMMENDATIONS AND APPLICATION\nGUIDANCE',
        features: [
          'Personalized scholarship recommendations',
          'Real-time eligibility checking',
          'Application deadline reminders',
          'Document requirement checklist',
          'Multi-language scholarship search',
          'Application status tracking'
        ]
      },
      hi: {
        title: 'स्कॉलरशिप\nचेकर',
        description: 'सर्वोत्तम छात्रवृत्ति के\nअवसर खोजें',
        subtext: 'व्यक्तिगत सिफारिशें और\nआवेदन मार्गदर्शन प्राप्त करें',
        features: [
          'व्यक्तिगत छात्रवृत्ति सिफारिशें',
          'वास्तविक समय पात्रता जांच',
          'आवेदन समय सीमा अनुस्मारक',
          'दस्तावेज़ आवश्यकता चेकलिस्ट',
          'बहु-भाषा छात्रवृत्ति खोज',
          'आवेदन स्थिति ट्रैकिंग'
        ]
      }
    }
  };

  return (
    <Container 
      maxWidth={false} 
      disableGutters 
      sx={{ 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a1929 0%, #102a43 100%)',
        overflowX: 'hidden',
        margin: 0,
        padding: 0,
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at top right, rgba(100, 181, 246, 0.1) 0%, transparent 50%)',
          pointerEvents: 'none',
          zIndex: 0,
        },
      }}
    >
      <Box sx={{ 
        maxWidth: '1920px', 
        margin: '0 auto',
        px: { xs: 2, sm: 3, md: 4, lg: 6 },
        py: { xs: 4, md: 6 },
        position: 'relative',
        zIndex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}>
        <Box sx={{ 
          position: { xs: 'relative', md: 'absolute' }, 
          top: { xs: 0, md: 40 },
          right: { xs: 0, md: 20 }, 
          display: 'flex', 
          flexDirection: { xs: 'column', md: 'row' },
          gap: { xs: 2, md: 3 }, 
          alignItems: 'center',
          justifyContent: { xs: 'center', md: 'flex-end' },
          width: { xs: '100%', md: 'auto' },
          mb: { xs: 6, md: 0 },
        }}>
          {/* Auth Buttons Container */}
          <Box sx={{
            display: 'flex',
            gap: { xs: 2, md: 2 },
            background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
            backdropFilter: 'blur(10px)',
            padding: { xs: '8px 16px', md: '8px 16px' },
            borderRadius: '30px',
            boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            width: { xs: '100%', md: 'auto' },
          }}>
            {!isLoggedIn ? (
              <>
                <Button
                  variant="contained"
                  onClick={() => setOpenSignUpDialog(true)}
                  sx={{
                    backgroundColor: '#64b5f6',
                    color: 'white',
                    borderRadius: '20px',
                    textTransform: 'none',
                    fontSize: { xs: '0.9rem', md: '1rem' },
                    px: { xs: 3, md: 4 },
                    py: 1,
                    flex: { xs: 1, md: 'none' },
                    minWidth: { xs: '120px', md: '140px' },
                    '&:hover': {
                      backgroundColor: '#1e88e5',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 5px 15px rgba(0,0,0,0.3)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Sign Up
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setOpenLoginDialog(true)}
                  sx={{
                    color: 'white',
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    borderRadius: '20px',
                    textTransform: 'none',
                    fontSize: { xs: '0.9rem', md: '1rem' },
                    px: { xs: 3, md: 4 },
                    py: 1,
                    flex: { xs: 1, md: 'none' },
                    minWidth: { xs: '120px', md: '140px' },
                    '&:hover': {
                      borderColor: '#64b5f6',
                      backgroundColor: 'rgba(100, 181, 246, 0.1)',
                      transform: 'translateY(-2px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Login
                </Button>
              </>
            ) : (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                {(() => {
                  const storedUser = JSON.parse(
                    localStorage.getItem('user') || '{}'
                  );
                  return storedUser?.picture ? (
                    <>
                      <Avatar 
                        src={storedUser.picture}
                        sx={{ width: 40, height: 40 }}
                      />
                      <Typography variant="caption" color="white">
                        {storedUser.name}
                      </Typography>
                    </>
                  ) : null;
                })()}
                <Button
                  variant="outlined"
                  onClick={logout}
                  sx={{
                    color: 'white',
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    borderRadius: '20px',
                    textTransform: 'none',
                    px: 6,
                    '&:hover': { borderColor: '#f44336', color: '#f44336', backgroundColor: 'rgba(244, 67, 54, 0.1)' }
                  }}
                >
                  Logout
                </Button>
              </Box>
            )}
          </Box>

          {/* Language Switcher Container */}
          <Box sx={{
            background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
            backdropFilter: 'blur(10px)',
            padding: { xs: '8px 16px', md: '8px 16px' },
            borderRadius: '30px',
            boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            width: { xs: '100%', md: 'auto' },
          }}>
            <Button
              variant="text"
              onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
              sx={{
                color: 'white',
                borderRadius: '20px',
                textTransform: 'none',
                fontSize: { xs: '0.9rem', md: '1rem' },
                px: { xs: 3, md: 4 },
                py: 1,
                width: '100%',
                minWidth: { xs: '120px', md: '140px' },
                opacity: 0.8,
                '&:hover': {
                  opacity: 1,
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  transform: 'translateY(-2px)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              {language === 'en' ? 'हिंदी' : 'English'}
            </Button>
          </Box>
        </Box>

        <Typography 
          variant="h1" 
          component="h1"
          sx={{
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #64b5f6 30%, #2196f3 90%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4.5rem' },
            width: '100%',
            textAlign: 'center',
            letterSpacing: { xs: '1px', md: '2px' },
            mb: { xs: 6, md: 10 },
            mt: { xs: 8, sm: 10, md: 12 },
            textShadow: '0 2px 10px rgba(100, 181, 246, 0.3)',
            animation: 'fadeIn 1s ease-out',
            '@keyframes fadeIn': {
              from: {
                opacity: 0,
                transform: 'translateY(-20px)',
              },
              to: {
                opacity: 1,
                transform: 'translateY(0)',
              },
            },
          }}
        >
          {language === 'en' ? 'Choose Your Service' : 'अपनी सेवा चुनें'}
        </Typography>

        <Grid container spacing={4} justifyContent="center" alignItems="stretch" sx={{ maxWidth: '1400px', mx: 'auto' }}>
          <Grid item xs={12} md={6}>
            <Card
              onClick={() => handleServiceSelection('lawTeller', '/local-law')}
              sx={{
                height: '100%',
                minHeight: '500px',
                background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(21, 101, 192, 0.25) 100%)',
                backdropFilter: 'blur(10px)',
                borderRadius: '30px',
                cursor: 'pointer',
                position: 'relative',
                overflow: 'visible',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                '&:hover': {
                  transform: 'translateY(-8px) scale(1.02)',
                  boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
                  '& .icon-circle': {
                    transform: 'translateX(-50%) scale(1.1)',
                    boxShadow: '0 8px 16px rgba(33, 150, 243, 0.4)',
                  },
                  background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.2) 0%, rgba(21, 101, 192, 0.3) 100%)',
                },
              }}
            >
              <Box
                className="icon-circle"
                sx={{
                  position: 'absolute',
                  top: '-30px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  background: 'linear-gradient(45deg, #2196f3 0%, #1565c0 100%)',
                  borderRadius: '50%',
                  width: '80px',
                  height: '80px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 6px 16px rgba(33, 150, 243, 0.3)',
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                  border: '3px solid rgba(255, 255, 255, 0.2)',
                  zIndex: 2,
                }}
              >
                <GavelIcon sx={{ fontSize: 40, color: 'white' }} />
              </Box>
              <CardContent sx={{ 
                pt: 7,
                px: 4,
                pb: 4,
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
              }}>
                <Typography 
                  variant="h3" 
                  sx={{ 
                    color: 'white',
                    fontWeight: 800,
                    mb: 4,
                    fontSize: { xs: '2.5rem', md: '3rem' },
                    lineHeight: 1.2,
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                    textShadow: '0 2px 4px rgba(0,0,0,0.2)',
                    whiteSpace: 'pre-line',
                  }}
                >
                  {serviceIntros.lawTeller[language].title}
                </Typography>
                <Box sx={{
                  background: 'rgba(33, 150, 243, 0.1)',
                  borderRadius: '20px',
                  p: 3,
                  mb: 4,
                  border: '1px solid rgba(33, 150, 243, 0.2)',
                }}>
                  <Typography 
                    variant="h5" 
                    sx={{ 
                      color: '#90caf9',
                      mb: 2,
                      fontWeight: 600,
                      fontSize: { xs: '1.4rem', md: '1.6rem' },
                      lineHeight: 1.4,
                      letterSpacing: '0.02em',
                      whiteSpace: 'pre-line',
                    }}
                  >
                    {serviceIntros.lawTeller[language].description}
                  </Typography>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.8)',
                      fontSize: { xs: '1.1rem', md: '1.2rem' },
                      lineHeight: 1.5,
                      letterSpacing: '0.02em',
                      whiteSpace: 'pre-line',
                    }}
                  >
                    {serviceIntros.lawTeller[language].subtext}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card
              onClick={() => handleServiceSelection('scholarship', '/scholarship')}
              sx={{
                height: '100%',
                minHeight: '500px',
                background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(21, 101, 192, 0.25) 100%)',
                backdropFilter: 'blur(10px)',
                borderRadius: '30px',
                cursor: 'pointer',
                position: 'relative',
                overflow: 'visible',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                '&:hover': {
                  transform: 'translateY(-8px) scale(1.02)',
                  boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
                  '& .icon-circle': {
                    transform: 'translateX(-50%) scale(1.1)',
                    boxShadow: '0 8px 16px rgba(33, 150, 243, 0.4)',
                  },
                  background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.2) 0%, rgba(21, 101, 192, 0.3) 100%)',
                },
              }}
            >
              <Box
                className="icon-circle"
                sx={{
                  position: 'absolute',
                  top: '-30px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  background: 'linear-gradient(45deg, #2196f3 0%, #1565c0 100%)',
                  borderRadius: '50%',
                  width: '80px',
                  height: '80px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 6px 16px rgba(33, 150, 243, 0.3)',
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                  border: '3px solid rgba(255, 255, 255, 0.2)',
                  zIndex: 2,
                }}
              >
                <SchoolIcon sx={{ fontSize: 40, color: 'white' }} />
              </Box>
              <CardContent sx={{ 
                pt: 7,
                px: 4,
                pb: 4,
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
              }}>
                <Typography 
                  variant="h3" 
                  sx={{ 
                    color: 'white',
                    fontWeight: 800,
                    mb: 4,
                    fontSize: { xs: '2.5rem', md: '3rem' },
                    lineHeight: 1.2,
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                    textShadow: '0 2px 4px rgba(0,0,0,0.2)',
                    whiteSpace: 'pre-line',
                  }}
                >
                  {serviceIntros.scholarship[language].title}
                </Typography>
                <Box sx={{
                  background: 'rgba(33, 150, 243, 0.1)',
                  borderRadius: '20px',
                  p: 3,
                  mb: 4,
                  border: '1px solid rgba(33, 150, 243, 0.2)',
                }}>
                  <Typography 
                    variant="h5" 
                    sx={{ 
                      color: '#90caf9',
                      mb: 2,
                      fontWeight: 600,
                      fontSize: { xs: '1.4rem', md: '1.6rem' },
                      lineHeight: 1.4,
                      letterSpacing: '0.02em',
                      whiteSpace: 'pre-line',
                    }}
                  >
                    {serviceIntros.scholarship[language].description}
                  </Typography>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.8)',
                      fontSize: { xs: '1.1rem', md: '1.2rem' },
                      lineHeight: 1.5,
                      letterSpacing: '0.02em',
                      whiteSpace: 'pre-line',
                    }}
                  >
                    {serviceIntros.scholarship[language].subtext}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Typography 
          variant="h1" 
          component="h2"
          sx={{
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #64b5f6 30%, #2196f3 90%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontSize: { xs: '2rem', sm: '3rem', md: '4rem' },
            width: '100%',
            textAlign: 'center',
            letterSpacing: { xs: '1px', md: '2px' },
            mt: { xs: 10, md: 14 },
            mb: { xs: 6, md: 8 },
            textShadow: '0 2px 10px rgba(100, 181, 246, 0.3)',
          }}
        >
          {language === 'en' ? 'Why our AI in law is better?' : 'हमारा AI कानून में क्यों बेहतर है?'}
        </Typography>

        <Typography
          variant="h5"
          sx={{
            color: 'rgba(255, 255, 255, 0.9)',
            textAlign: 'center',
            mb: { xs: 8, md: 10 },
            maxWidth: '800px',
            mx: 'auto',
            px: 2,
            fontSize: { xs: '1.2rem', md: '1.4rem' },
            lineHeight: 1.6,
          }}
        >
          {language === 'en' 
            ? 'In contrast to others, our LegalTech software is quick, easy, and wallet-friendly.'
            : 'दूसरों की तुलना में, हमारा लीगलटेक सॉफ्टवेयर त्वरित, आसान और किफायती है।'
          }
        </Typography>

        <Grid container spacing={4} sx={{ maxWidth: '1400px', mx: 'auto', px: { xs: 2, md: 4 } }}>
          {/* Time Saved Card */}
          <Grid item xs={12} md={6} lg={3}>
            <Card sx={{
              background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(21, 101, 192, 0.25) 100%)',
              backdropFilter: 'blur(10px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              p: 4,
              transition: 'transform 0.3s ease-in-out',
              '&:hover': {
                transform: 'translateY(-8px)',
                boxShadow: '0 12px 24px rgba(0, 0, 0, 0.2)',
              },
            }}>
              <Typography variant="h2" sx={{
                color: '#64b5f6',
                fontWeight: 'bold',
                fontSize: { xs: '3.5rem', md: '4rem' },
                mb: 2,
              }}>
                75%
              </Typography>
              <Typography variant="h5" sx={{
                color: 'white',
                textAlign: 'center',
                fontWeight: 600,
                mb: 2,
              }}>
                {language === 'en' ? 'Time saved' : 'समय की बचत'}
              </Typography>
              <Typography sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textAlign: 'center',
                fontSize: '1.1rem',
              }}>
                {language === 'en' ? 'On routine tasks' : 'नियमित कार्यों पर'}
              </Typography>
            </Card>
          </Grid>

          {/* Cost Reduction Card */}
          <Grid item xs={12} md={6} lg={3}>
            <Card sx={{
              background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(21, 101, 192, 0.25) 100%)',
              backdropFilter: 'blur(10px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              p: 4,
              transition: 'transform 0.3s ease-in-out',
              '&:hover': {
                transform: 'translateY(-8px)',
                boxShadow: '0 12px 24px rgba(0, 0, 0, 0.2)',
              },
            }}>
              <Typography variant="h2" sx={{
                color: '#64b5f6',
                fontWeight: 'bold',
                fontSize: { xs: '3.5rem', md: '4rem' },
                mb: 2,
              }}>
                90%
              </Typography>
              <Typography variant="h5" sx={{
                color: 'white',
                textAlign: 'center',
                fontWeight: 600,
                mb: 2,
              }}>
                {language === 'en' ? 'Cost reduction' : 'लागत में कमी'}
              </Typography>
              <Typography sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textAlign: 'center',
                fontSize: '1.1rem',
              }}>
                {language === 'en' ? 'In legal services' : 'कानूनी सेवाओं में'}
              </Typography>
            </Card>
          </Grid>

          {/* Fast Processing Card */}
          <Grid item xs={12} md={6} lg={3}>
            <Card sx={{
              background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(21, 101, 192, 0.25) 100%)',
              backdropFilter: 'blur(10px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              p: 4,
              transition: 'transform 0.3s ease-in-out',
              '&:hover': {
                transform: 'translateY(-8px)',
                boxShadow: '0 12px 24px rgba(0, 0, 0, 0.2)',
              },
            }}>
              <Typography variant="h2" sx={{
                color: '#64b5f6',
                fontWeight: 'bold',
                fontSize: { xs: '3.5rem', md: '4rem' },
                mb: 2,
              }}>
                5s
              </Typography>
              <Typography variant="h5" sx={{
                color: 'white',
                textAlign: 'center',
                fontWeight: 600,
                mb: 2,
              }}>
                {language === 'en' ? 'Processing time' : 'प्रोसेसिंग समय'}
              </Typography>
              <Typography sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textAlign: 'center',
                fontSize: '1.1rem',
              }}>
                {language === 'en' ? 'To summarize any document' : 'किसी भी दस्तावेज़ को संक्षेप में'}
              </Typography>
            </Card>
          </Grid>

          {/* 24/7 Support Card */}
          <Grid item xs={12} md={6} lg={3}>
            <Card sx={{
              background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(21, 101, 192, 0.25) 100%)',
              backdropFilter: 'blur(10px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              p: 4,
              transition: 'transform 0.3s ease-in-out',
              '&:hover': {
                transform: 'translateY(-8px)',
                boxShadow: '0 12px 24px rgba(0, 0, 0, 0.2)',
              },
            }}>
              <Typography variant="h2" sx={{
                color: '#64b5f6',
                fontWeight: 'bold',
                fontSize: { xs: '3.5rem', md: '4rem' },
                mb: 2,
              }}>
                24/7
              </Typography>
              <Typography variant="h5" sx={{
                color: 'white',
                textAlign: 'center',
                fontWeight: 600,
                mb: 2,
              }}>
                {language === 'en' ? 'Support' : 'सहायता'}
              </Typography>
              <Typography sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textAlign: 'center',
                fontSize: '1.1rem',
              }}>
                {language === 'en' ? 'Always available to assist you' : 'हमेशा आपकी मदद के लिए उपलब्ध'}
              </Typography>
            </Card>
          </Grid>
        </Grid>

        <Typography 
          variant="h1" 
          component="h2"
          sx={{
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #64b5f6 30%, #2196f3 90%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontSize: { xs: '2rem', sm: '3rem', md: '4rem' },
            width: '100%',
            textAlign: 'center',
            letterSpacing: { xs: '1px', md: '2px' },
            mt: { xs: 10, md: 14 },
            mb: { xs: 6, md: 10 },
            textShadow: '0 2px 10px rgba(100, 181, 246, 0.3)',
          }}
        >
          {language === 'en' ? 'Key Features' : 'मुख्य विशेषताएं'}
        </Typography>

        <Grid container spacing={{ xs: 4, md: 6 }} justifyContent="center" sx={{ 
          width: '100%', 
          mx: 'auto',
          px: { xs: 2, md: 4 },
          maxWidth: '1600px',
          mt: { xs: 6, md: 8 }
        }}>
          <Grid item xs={12} md={6} sx={{ 
            display: 'flex',
            alignItems: 'stretch',
          }}>
            <Card
              sx={{
                background: 'rgba(13, 71, 161, 0.4)',
                backdropFilter: 'blur(10px)',
                borderRadius: '20px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                height: '100%',
                display: 'flex',
                flexDirection: 'column'
              }}
            >
              <CardContent sx={{ p: { xs: 3, md: 4 } }}>
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  mb: { xs: 4, md: 5 },
                  gap: 2,
                  borderBottom: '2px solid rgba(255, 255, 255, 0.1)',
                  pb: 2
                }}>
                  <GavelIcon sx={{ 
                    fontSize: { xs: 35, md: 40 }, 
                    color: '#64b5f6',
                  }} />
                  <Typography 
                    variant="h4" 
                    component="h3" 
                    sx={{ 
                      color: '#64b5f6',
                      fontWeight: 'bold',
                      fontSize: { xs: '1.8rem', sm: '2rem', md: '2.2rem' },
                    }}
                  >
                    {language === 'en' ? 'Local Law Teller Features' : 'लोकल लॉ टेलर विशेषताएं'}
                  </Typography>
                </Box>
                <List sx={{ 
                  px: { xs: 2, md: 3 },
                  '& .MuiListItem-root': {
                    px: 3,
                    py: 2,
                    display: 'flex',
                    alignItems: 'center',
                    mb: 2,
                    '&:before': {
                      content: '"•"',
                      color: '#64b5f6',
                      fontSize: '2rem',
                      marginRight: '16px',
                      fontWeight: 'bold',
                      lineHeight: 1
                    }
                  }
                }}>
                  {serviceIntros.lawTeller[language].features.map((feature, index) => (
                    <ListItem 
                      key={index}
                      sx={{ 
                        color: 'rgba(255, 255, 255, 0.95)',
                        fontSize: { xs: '1.2rem', md: '1.3rem' },
                        fontWeight: '500',
                        letterSpacing: '0.5px',
                        lineHeight: '1.5',
                        borderRadius: '12px',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          background: 'rgba(255, 255, 255, 0.1)',
                          transform: 'translateX(5px)',
                        }
                      }}
                    >
                      {feature}
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6} sx={{ 
            display: 'flex',
            alignItems: 'stretch',
          }}>
            <Card
              sx={{
                background: 'rgba(13, 71, 161, 0.4)',
                backdropFilter: 'blur(10px)',
                borderRadius: '20px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                height: '100%',
                display: 'flex',
                flexDirection: 'column'
              }}
            >
              <CardContent sx={{ p: { xs: 3, md: 4 } }}>
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  mb: { xs: 4, md: 5 },
                  gap: 2,
                  borderBottom: '2px solid rgba(255, 255, 255, 0.1)',
                  pb: 2
                }}>
                  <SchoolIcon sx={{ 
                    fontSize: { xs: 35, md: 40 }, 
                    color: '#64b5f6',
                  }} />
                  <Typography 
                    variant="h4" 
                    component="h3" 
                    sx={{ 
                      color: '#64b5f6',
                      fontWeight: 'bold',
                      fontSize: { xs: '1.8rem', sm: '2rem', md: '2.2rem' },
                    }}
                  >
                    {language === 'en' ? 'Scholarship Checker Features' : 'स्कॉलरशिप चेकर विशेषताएं'}
                  </Typography>
                </Box>
                <List sx={{ 
                  px: { xs: 2, md: 3 },
                  '& .MuiListItem-root': {
                    px: 3,
                    py: 2,
                    display: 'flex',
                    alignItems: 'center',
                    mb: 2,
                    '&:before': {
                      content: '"•"',
                      color: '#64b5f6',
                      fontSize: '2rem',
                      marginRight: '16px',
                      fontWeight: 'bold',
                      lineHeight: 1
                    }
                  }
                }}>
                  {serviceIntros.scholarship[language].features.map((feature, index) => (
                    <ListItem 
                      key={index}
                      sx={{ 
                        color: 'rgba(255, 255, 255, 0.95)',
                        fontSize: { xs: '1.2rem', md: '1.3rem' },
                        fontWeight: '500',
                        letterSpacing: '0.5px',
                        lineHeight: '1.5',
                        borderRadius: '12px',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          background: 'rgba(255, 255, 255, 0.1)',
                          transform: 'translateX(5px)',
                        }
                      }}
                    >
                      {feature}
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* FAQ Section */}
        <Box sx={{ 
          width: '100%', 
          maxWidth: '1400px', 
          mx: 'auto',
          mt: { xs: 10, md: 14 },
          mb: { xs: 8, md: 12 },
          px: { xs: 2, md: 4 },
        }}>
          <Typography 
            variant="h2" 
            sx={{
              textAlign: 'center',
              fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
              fontWeight: 'bold',
              color: 'white',
              mb: { xs: 4, md: 6 },
            }}
          >
            {language === 'en' ? 'Have a question?' : 'कोई सवाल है?'}
          </Typography>
          
          <Typography
            variant="h6"
            sx={{
              textAlign: 'center',
              color: 'rgba(255, 255, 255, 0.7)',
              mb: { xs: 6, md: 8 },
              fontSize: { xs: '1rem', md: '1.1rem' },
            }}
          >
            {language === 'en' ? 'Browse through our frequently asked topics.' : 'हमारे अक्सर पूछे जाने वाले विषयों को ब्राउज़ करें।'}
          </Typography>

          <Box sx={{ maxWidth: '900px', mx: 'auto' }}>
            {faqData[language].map((faq, index) => (
              <Accordion
                key={index}
                expanded={expanded === `panel${index}`}
                onChange={handleAccordionChange(`panel${index}`)}
                sx={{
                  background: 'rgba(13, 71, 161, 0.3)',
                  backdropFilter: 'blur(10px)',
                  color: 'white',
                  borderRadius: '16px !important',
                  mb: 2,
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  '&:before': {
                    display: 'none',
                  },
                  '&.Mui-expanded': {
                    margin: '0 0 16px 0',
                    background: 'rgba(13, 71, 161, 0.4)',
                    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
                  },
                  transition: 'all 0.3s ease',
                }}
              >
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon sx={{ color: '#64b5f6' }} />}
                  sx={{
                    '& .MuiAccordionSummary-content': {
                      my: 2,
                    },
                    '&:hover': {
                      background: 'rgba(255, 255, 255, 0.05)',
                    },
                  }}
                >
                  <Typography sx={{ 
                    fontSize: { xs: '1.1rem', md: '1.2rem' },
                    fontWeight: 600,
                    color: '#90caf9',
                  }}>
                    {faq.question}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails sx={{ 
                  borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                  py: 3,
                }}>
                  <Typography sx={{ 
                    color: 'rgba(255, 255, 255, 0.9)',
                    fontSize: { xs: '1rem', md: '1.1rem' },
                    lineHeight: 1.6,
                  }}>
                    {faq.answer}
                  </Typography>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        </Box>

        {/* Dialogs and Snackbar */}
        <Dialog 
          open={openSignUpDialog} 
          onClose={() => setOpenSignUpDialog(false)}
          PaperProps={{
            sx: {
              background: 'linear-gradient(135deg, rgba(13, 71, 161, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%)',
              backdropFilter: 'blur(20px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              minWidth: { xs: '90%', sm: '400px' },
              margin: { xs: 2, sm: 0 },
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
              overflow: 'hidden',
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'radial-gradient(circle at top right, rgba(255,255,255,0.2) 0%, transparent 60%)',
                pointerEvents: 'none',
              },
            }
          }}
          fullScreen={false}
          maxWidth="sm"
          TransitionProps={{
            timeout: 500,
          }}
        >
          <DialogTitle sx={{ color: 'white', textAlign: 'center', pb: 1, position: 'relative' }}>
            Sign Up
            <IconButton
              aria-label="close"
              onClick={() => setOpenSignUpDialog(false)}
              sx={{
                position: 'absolute',
                right: 8,
                top: 8,
                color: 'rgba(255, 255, 255, 0.7)',
                '&:hover': {
                  color: 'white',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
              }}
            >
              <CloseIcon />
            </IconButton>
          </DialogTitle>
          <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
            <TextField
              autoFocus
              margin="dense"
              label="Email Address"
              type="email"
              fullWidth
              value={signUpData.email}
              onChange={(e) => setSignUpData({ ...signUpData, email: e.target.value })}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: 'white',
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#64b5f6',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                  '&.Mui-focused': {
                    color: '#64b5f6',
                  },
                },
              }}
            />
            <TextField
              margin="dense"
              label="Password"
              type="password"
              fullWidth
              value={signUpData.password}
              onChange={(e) => setSignUpData({ ...signUpData, password: e.target.value })}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: 'white',
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#64b5f6',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                  '&.Mui-focused': {
                    color: '#64b5f6',
                  },
                },
              }}
            />
            <Button
              variant="contained"
              onClick={handleSignUp}
              fullWidth
              sx={{
                mt: 2,
                backgroundColor: '#64b5f6',
                color: 'white',
                '&:hover': {
                  backgroundColor: '#1e88e5',
                },
              }}
            >
              SIGN UP
            </Button>
            
            <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
              <Divider sx={{ flex: 1, borderColor: 'rgba(255, 255, 255, 0.3)' }} />
              <Typography sx={{ mx: 2, color: 'rgba(255, 255, 255, 0.7)' }}>or</Typography>
              <Divider sx={{ flex: 1, borderColor: 'rgba(255, 255, 255, 0.3)' }} />
            </Box>

            <Button
              variant="contained"
              startIcon={<GoogleIcon />}
              onClick={handleGoogleSignUp}
              fullWidth
              sx={{
                backgroundColor: '#fff',
                color: '#757575',
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                },
              }}
            >
              Sign up with Google
            </Button>
          </DialogContent>
          <DialogActions sx={{ justifyContent: 'center', pb: 3 }}>
            <Button 
              onClick={() => setOpenSignUpDialog(false)}
              sx={{ color: 'rgba(255, 255, 255, 0.7)' }}
            >
              Cancel
            </Button>
          </DialogActions>
        </Dialog>

        <Dialog 
          open={openLoginDialog} 
          onClose={() => setOpenLoginDialog(false)}
          PaperProps={{
            sx: {
              background: 'linear-gradient(135deg, rgba(13, 71, 161, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%)',
              backdropFilter: 'blur(20px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              minWidth: { xs: '90%', sm: '400px' },
              margin: { xs: 2, sm: 0 },
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
              overflow: 'hidden',
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'radial-gradient(circle at top right, rgba(255,255,255,0.2) 0%, transparent 60%)',
                pointerEvents: 'none',
              },
            }
          }}
          fullScreen={false}
          maxWidth="sm"
          TransitionProps={{
            timeout: 500,
          }}
        >
          <DialogTitle sx={{ color: 'white', textAlign: 'center', pb: 1, position: 'relative' }}>
            Login
            <IconButton
              aria-label="close"
              onClick={() => setOpenLoginDialog(false)}
              sx={{
                position: 'absolute',
                right: 8,
                top: 8,
                color: 'rgba(255, 255, 255, 0.7)',
                '&:hover': {
                  color: 'white',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
              }}
            >
              <CloseIcon />
            </IconButton>
          </DialogTitle>
          <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
            <TextField
              autoFocus
              margin="dense"
              label="Email Address"
              type="email"
              fullWidth
              value={loginData.email}
              onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: 'white',
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#64b5f6',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                  '&.Mui-focused': {
                    color: '#64b5f6',
                  },
                },
              }}
            />
            <TextField
              margin="dense"
              label="Password"
              type="password"
              fullWidth
              value={loginData.password}
              onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: 'white',
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#64b5f6',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                  '&.Mui-focused': {
                    color: '#64b5f6',
                  },
                },
              }}
            />
            <Button
              variant="contained"
              onClick={handleLogin}
              fullWidth
              sx={{
                mt: 2,
                backgroundColor: '#64b5f6',
                color: 'white',
                '&:hover': {
                  backgroundColor: '#1e88e5',
                },
              }}
            >
              LOGIN
            </Button>
            
            <Divider sx={{ my: 2 }}>
              <Typography color="rgba(255, 255, 255, 0.7)" variant="caption">
                OR CONTINUE WITH
              </Typography>
            </Divider>
            
            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleError}
                theme="filled_black"
                size="large"
                text="signin_with"
                shape="rectangular"
              />
            </Box>
          </DialogContent>
          <DialogActions sx={{ justifyContent: 'center', pb: 3 }}>
            <Button 
              onClick={() => setOpenLoginDialog(false)}
              sx={{ color: 'rgba(255, 255, 255, 0.7)' }}
            >
              Cancel
            </Button>
          </DialogActions>
        </Dialog>

        <Snackbar
          open={openNotification}
          autoHideDuration={2000}
          onClose={() => setOpenNotification(false)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert
            severity="success"
            variant="filled"
            sx={{
              background: 'linear-gradient(135deg, rgba(13, 71, 161, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%)',
              backdropFilter: 'blur(10px)',
              borderRadius: '20px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
              minWidth: { xs: '90vw', sm: '400px' },
              padding: '16px 24px',
              '& .MuiAlert-icon': {
                color: '#64b5f6',
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))',
              },
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'radial-gradient(circle at top right, rgba(255,255,255,0.2) 0%, transparent 60%)',
                pointerEvents: 'none',
                borderRadius: '20px',
              },
            }}
          >
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                sx={{
                  fontSize: { xs: '1.3rem', sm: '1.4rem' },
                  fontWeight: 'bold',
                  color: '#fff',
                  mb: 1,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  textShadow: '0 2px 4px rgba(0,0,0,0.2)'
                }}
              >
                {selectedService === 'lawTeller' ? 'You have selected Local Law Teller' : 'You have selected Scholarship Checker'}
              </Typography>
              <Typography
                sx={{
                  fontSize: { xs: '1.2rem', sm: '1.3rem' },
                  color: '#90caf9',
                  mb: 2,
                  fontWeight: 500
                }}
              >
                {selectedService === 'lawTeller' ? 'आपने लोकल लॉ टेलर चुना है' : 'आपने स्कॉलरशिप चेकर चुना है'}
              </Typography>
              <Divider sx={{ 
                my: 1.5, 
                borderColor: 'rgba(255, 255, 255, 0.2)',
                width: '80%',
                mx: 'auto'
              }} />
              <Typography
                sx={{
                  fontSize: '1rem',
                  color: 'rgba(255, 255, 255, 0.8)',
                  mt: 1,
                  fontStyle: 'italic'
                }}
              >
                {selectedService && `${serviceIntros[selectedService]['en'].description}\n${serviceIntros[selectedService]['hi'].description}`}
              </Typography>
            </Box>
          </Alert>
        </Snackbar>

        <Snackbar
          open={openError}
          autoHideDuration={4000}
          onClose={() => setOpenError(false)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert 
            onClose={() => setOpenError(false)} 
            severity="warning" 
            variant="filled"
            sx={{ 
              width: '100%',
              borderRadius: '15px',
              fontFamily: 'Inter, sans-serif'
            }}
          >
            Please login to access this feature.
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
};

export default ServiceSelection; 