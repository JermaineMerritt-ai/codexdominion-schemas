import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'screens/dashboard_screen.dart';
import 'services/api_client.dart';
import 'services/websocket_service.dart';
import 'services/push_notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp();

  // Initialize Hive for local storage
  await Hive.initFlutter();

  // Initialize push notifications
  final pushService = PushNotificationService();
  await pushService.initialize();

  runApp(const CodexDominionApp());
}

class CodexDominionApp extends StatelessWidget {
  const CodexDominionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<ApiClient>(
          create: (_) => ApiClient(baseUrl: 'http://localhost:5555'),
        ),
        Provider<WebSocketService>(
          create: (_) => WebSocketService(url: 'ws://localhost:8765'),
        ),
        Provider<PushNotificationService>(
          create: (_) => PushNotificationService(),
        ),
      ],
      child: MaterialApp(
        title: 'Codex Dominion',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Color(int.parse('#667eea'.substring(1), radix: 16) + 0xFF000000),
            secondary: Color(int.parse('#764ba2'.substring(1), radix: 16) + 0xFF000000),
          ),
          useMaterial3: true,
          appBarTheme: AppBarTheme(
            centerTitle: true,
            elevation: 2,
            backgroundColor: Color(int.parse('#667eea'.substring(1), radix: 16) + 0xFF000000),
            foregroundColor: Colors.white,
          ),
        ),
        home: const DashboardScreen(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
