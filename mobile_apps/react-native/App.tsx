import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import MainNavigator from './src/navigation/MainNavigator';
import { ApiProvider } from './src/services/ApiContext';
import { WebSocketProvider } from './src/services/WebSocketContext';

const App = () => {
  return (
    <SafeAreaProvider>
      <ApiProvider>
        <WebSocketProvider>
          <NavigationContainer>
            <MainNavigator />
          </NavigationContainer>
        </WebSocketProvider>
      </ApiProvider>
    </SafeAreaProvider>
  );
};

export default App;
