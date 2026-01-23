import React from 'react';
import {
  Box,
  Typography,
  Stack,
} from '@mui/material';

const RelatedContent = ({ serviceType }) => {
  const blogPosts = serviceType === 'lawTeller' ? [
    {
      title: 'Understanding Property Rights in India',
      description: 'An in-depth analysis of property rights, inheritance laws, and real estate regulations in India. Learn about your rights as a property owner and how to protect your interests.',
      readTime: '8 min read',
      date: 'Feb 15, 2024',
      tags: ['Property Law', 'Real Estate', 'Inheritance', 'Legal Rights']
    },
    {
      title: 'Consumer Protection Act 2019',
      description: 'Everything you need to know about the new Consumer Protection Act and how it strengthens consumer rights. Includes case studies and practical examples.',
      readTime: '10 min read',
      date: 'Feb 12, 2024',
      tags: ['Consumer Law', 'Legal Rights', 'Case Studies', 'Latest Updates']
    },
    {
      title: 'Employment Law Guide',
      description: 'A comprehensive guide to employment laws, workplace rights, and dispute resolution. Learn about contracts, compensation, and legal remedies.',
      readTime: '12 min read',
      date: 'Feb 10, 2024',
      tags: ['Employment Law', 'Workplace Rights', 'Contracts', 'Dispute Resolution']
    }
  ] : [
    {
      title: 'Government Scholarship Programs 2024',
      description: 'Detailed overview of all major government scholarship schemes, eligibility criteria, and application processes. Including new programs and deadline updates.',
      readTime: '15 min read',
      date: 'Feb 15, 2024',
      tags: ['Government Aid', 'Financial Support', 'Deadlines', '2024 Updates']
    },
    {
      title: 'International Scholarship Guide',
      description: 'Complete guide to securing international scholarships. Includes tips for SOP writing, recommendation letters, and interview preparation.',
      readTime: '20 min read',
      date: 'Feb 13, 2024',
      tags: ['Study Abroad', 'Application Tips', 'SOP Writing', 'Interviews']
    },
    {
      title: 'Merit Scholarship Success Stories',
      description: 'Real stories from successful scholarship recipients, including their preparation strategies, challenges faced, and tips for future applicants.',
      readTime: '10 min read',
      date: 'Feb 11, 2024',
      tags: ['Success Stories', 'Merit Based', 'Strategy', 'Tips & Tricks']
    }
  ];

  return (
    <Box sx={{ 
      width: '100%',
      p: { xs: 3, md: 4 },
      background: 'linear-gradient(145deg, rgba(10, 25, 41, 0.7) 0%, rgba(15, 40, 80, 0.8) 100%)',
      borderRadius: '24px',
      backdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
    }}>
      <Typography 
        variant="h5" 
        sx={{ 
          color: '#fff',
          mb: 4,
          fontWeight: 700,
          fontSize: { xs: '1.5rem', md: '1.75rem' },
          textAlign: 'center',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          background: 'linear-gradient(90deg, #64b5f6 0%, #2196f3 100%)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        Related Content
      </Typography>

      <Stack spacing={3}>
        {blogPosts.map((post, index) => (
          <Box
            key={index}
            sx={{
              p: 3,
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
              borderRadius: '16px',
              border: '1px solid rgba(255, 255, 255, 0.05)',
              transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
              cursor: 'pointer',
              position: 'relative',
              overflow: 'hidden',
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(33, 150, 243, 0) 100%)',
                opacity: 0,
                transition: 'opacity 0.4s ease',
              },
              '&:hover': {
                transform: 'translateY(-4px) scale(1.01)',
                boxShadow: '0 8px 30px rgba(0, 0, 0, 0.12)',
                '&::before': {
                  opacity: 1,
                },
              }
            }}
          >
            <Typography 
              variant="h6" 
              sx={{ 
                color: '#90caf9',
                fontWeight: 700,
                mb: 2,
                fontSize: { xs: '1.1rem', md: '1.2rem' },
                lineHeight: 1.4,
              }}
            >
              {post.title}
            </Typography>
            <Typography 
              variant="body1" 
              sx={{ 
                color: 'rgba(255, 255, 255, 0.85)',
                mb: 2.5,
                lineHeight: 1.6,
                fontSize: { xs: '0.95rem', md: '1rem' },
              }}
            >
              {post.description}
            </Typography>
            <Stack 
              direction="row" 
              spacing={1} 
              sx={{ 
                mb: 3, 
                flexWrap: 'wrap', 
                gap: 1 
              }}
            >
              {post.tags.map((tag, tagIndex) => (
                <Box
                  key={tagIndex}
                  sx={{
                    background: 'rgba(33, 150, 243, 0.1)',
                    color: '#64b5f6',
                    px: 2,
                    py: 0.75,
                    borderRadius: '20px',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    letterSpacing: '0.02em',
                    border: '1px solid rgba(33, 150, 243, 0.15)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      background: 'rgba(33, 150, 243, 0.2)',
                      transform: 'translateY(-1px)',
                    }
                  }}
                >
                  {tag}
                </Box>
              ))}
            </Stack>
            <Stack 
              direction="row" 
              spacing={3} 
              alignItems="center"
              sx={{
                borderTop: '1px solid rgba(255, 255, 255, 0.05)',
                pt: 2,
              }}
            >
              <Typography 
                variant="caption" 
                sx={{ 
                  color: 'rgba(255, 255, 255, 0.6)',
                  fontSize: '0.85rem',
                  fontWeight: 500,
                }}
              >
                {post.date}
              </Typography>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: 'rgba(255, 255, 255, 0.6)',
                  fontSize: '0.85rem',
                  fontWeight: 500,
                }}
              >
                {post.readTime}
              </Typography>
            </Stack>
          </Box>
        ))}
      </Stack>
    </Box>
  );
};

export default RelatedContent; 