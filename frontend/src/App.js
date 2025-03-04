import React from 'react';
import { ChakraProvider, Box, Container, VStack } from '@chakra-ui/react';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header';
import theme from './theme';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <VStack minH="100vh" spacing={0}>
        <Header />
        <Box flex="1" w="full" bg="gray.50" py={8}>
          <Container maxW="container.lg">
            <ChatInterface />
          </Container>
        </Box>
      </VStack>
    </ChakraProvider>
  );
}

export default App; 