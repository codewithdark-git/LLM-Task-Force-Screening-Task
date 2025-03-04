import React from 'react';
import { Box } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';

const bounceAnimation = keyframes`
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
`;

const LoadingDots = () => {
  const dots = Array(3).fill(0);

  return (
    <Box display="flex" justifyContent="center" alignItems="center" gap={1} h="24px">
      {dots.map((_, i) => (
        <Box
          key={i}
          as="span"
          h="6px"
          w="6px"
          bg="brand.500"
          borderRadius="full"
          display="inline-block"
          animation={`${bounceAnimation} 1.4s infinite ease-in-out both`}
          style={{ animationDelay: `${i * 0.16}s` }}
        />
      ))}
    </Box>
  );
};

export default LoadingDots; 