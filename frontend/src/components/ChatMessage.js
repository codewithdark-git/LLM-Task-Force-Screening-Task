import React from 'react';
import { Box, Text, VStack, Badge, Flex, Tooltip } from '@chakra-ui/react';
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ message, isUser }) => {
  return (
    <Flex justify={isUser ? 'flex-end' : 'flex-start'}>
      <Box
        maxW="70%"
        bg={isUser ? 'brand.500' : 'gray.100'}
        color={isUser ? 'white' : 'black'}
        p={3}
        borderRadius="lg"
        boxShadow="sm"
      >
        <VStack align="stretch" spacing={2}>
          <Text>
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </Text>
          
          {!isUser && message.sources && message.sources.length > 0 && (
            <Box mt={2} pt={2} borderTopWidth="1px" borderColor={isUser ? 'whiteAlpha.300' : 'gray.200'}>
              <Text fontSize="xs" color={isUser ? 'whiteAlpha.700' : 'gray.500'} mb={1}>
                Sources:
              </Text>
              <Flex wrap="wrap" gap={1}>
                {message.sources.map((source, index) => (
                  <Tooltip 
                    key={index}
                    label={source.topic ? `Topic: ${source.topic}` : source.source}
                    placement="top"
                    hasArrow
                  >
                    <Badge
                      colorScheme={source.source.includes("FAQ") ? "green" : "blue"}
                      fontSize="xs"
                      cursor="pointer"
                      variant={isUser ? 'solid' : 'subtle'}
                    >
                      {source.category || source.source}
                    </Badge>
                  </Tooltip>
                ))}
              </Flex>
            </Box>
          )}
        </VStack>
      </Box>
    </Flex>
  );
};

export default ChatMessage; 