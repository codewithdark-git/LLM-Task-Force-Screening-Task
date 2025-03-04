import React from 'react';
import { Box, Flex, Text, Image, useColorModeValue } from '@chakra-ui/react';

const Header = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box
      as="header"
      bg={bgColor}
      borderBottom="1px"
      borderColor={borderColor}
      py={4}
      px={8}
      position="sticky"
      top={0}
      zIndex={10}
    >
      <Flex maxW="container.lg" mx="auto" align="center" justify="space-between">
        <Flex align="center">
          <Image
            src="/jiopay-logo.png"
            alt="JioPay Logo"
            height="32px"
            fallbackSrc="https://via.placeholder.com/32x32"
            mr={3}
          />
          <Text fontSize="xl" fontWeight="bold" bgGradient="linear(to-r, brand.500, brand.300)" bgClip="text">
            Support Assistant
          </Text>
        </Flex>
        <Text fontSize="sm" color="gray.500">
          Powered by AI
        </Text>
      </Flex>
    </Box>
  );
};

export default Header; 