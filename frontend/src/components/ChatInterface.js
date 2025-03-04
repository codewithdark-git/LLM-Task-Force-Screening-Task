import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  VStack,
  Input,
  IconButton,
  Flex,
  Text,
  useToast,
  InputGroup,
  InputRightElement,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiSend } from 'react-icons/fi';
import axios from 'axios';
import ChatMessage from './ChatMessage';
import LoadingDots from './LoadingDots';

const INITIAL_MESSAGE = {
  role: 'assistant',
  content: 'Hello! I`m your JioPay Support Assistant. How can I help you today?'
};

const ChatInterface = () => {
  const [messages, setMessages] = useState([INITIAL_MESSAGE]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const toast = useToast();
  const inputBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: input,
        chat_history: messages.filter(msg => msg !== INITIAL_MESSAGE), // Exclude initial greeting
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        sources: response.data.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to get response from the chatbot.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      bg="white"
      height="75vh"
      display="flex"
      flexDirection="column"
      boxShadow="sm"
    >
      <Box p={4} borderBottomWidth="1px" bg="gray.50">
        <Text fontSize="lg" fontWeight="medium">
          Chat Support
        </Text>
      </Box>

      <VStack
        flex="1"
        overflowY="auto"
        spacing={4}
        p={4}
        alignItems="stretch"
        css={{
          '&::-webkit-scrollbar': {
            width: '8px',
          },
          '&::-webkit-scrollbar-track': {
            width: '10px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'var(--chakra-colors-gray-200)',
            borderRadius: '24px',
          },
        }}
      >
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message}
            isUser={message.role === 'user'}
          />
        ))}
        {isLoading && (
          <Flex justify="flex-start">
            <Box
              maxW="70%"
              bg="gray.100"
              p={3}
              borderRadius="lg"
            >
              <LoadingDots />
            </Box>
          </Flex>
        )}
        <div ref={messagesEndRef} />
      </VStack>

      <Box p={4} borderTopWidth="1px" borderColor={borderColor}>
        <InputGroup size="lg">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            bg={inputBg}
            disabled={isLoading}
            _disabled={{ opacity: 0.7 }}
            pr="4.5rem"
          />
          <InputRightElement width="4.5rem">
            <IconButton
              h="1.75rem"
              size="sm"
              icon={<FiSend />}
              onClick={handleSend}
              isLoading={isLoading}
              colorScheme="brand"
              aria-label="Send message"
              isDisabled={!input.trim()}
            />
          </InputRightElement>
        </InputGroup>
      </Box>
    </Box>
  );
};

export default ChatInterface; 