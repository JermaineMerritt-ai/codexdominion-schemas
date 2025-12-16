import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import HomeScreen from '../screens/HomeScreen';
import SocialScreen from '../screens/SocialScreen';
import AffiliateScreen from '../screens/AffiliateScreen';
import ChatScreen from '../screens/ChatScreen';
import SettingsScreen from '../screens/SettingsScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const MainNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName = 'home';

          if (route.name === 'Home') iconName = 'home';
          else if (route.name === 'Social') iconName = 'share';
          else if (route.name === 'Affiliate') iconName = 'attach-money';
          else if (route.name === 'Chat') iconName = 'forum';
          else if (route.name === 'Settings') iconName = 'settings';

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#667eea',
        tabBarInactiveTintColor: 'gray',
        headerStyle: {
          backgroundColor: '#667eea',
        },
        headerTintColor: '#fff',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Social" component={SocialScreen} />
      <Tab.Screen name="Affiliate" component={AffiliateScreen} />
      <Tab.Screen name="Chat" component={ChatScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
};

export default MainNavigator;
