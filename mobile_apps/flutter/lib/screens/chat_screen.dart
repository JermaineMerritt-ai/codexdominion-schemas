import 'package:flutter/material.dart';

class WebSocketChatScreen extends StatelessWidget {
  const WebSocketChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('WebSocket Chat'),
      ),
      body: Center(
        child: Text('WebSocket Chat Content Here'),
      ),
    );
  }
}
