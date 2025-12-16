import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:convert';

class WebSocketService {
  final String url;
  WebSocketChannel? _channel;

  WebSocketService({required this.url});

  void connect() {
    _channel = WebSocketChannel.connect(Uri.parse(url));

    // Authenticate
    _channel!.sink.add(json.encode({
      'type': 'auth',
      'username': 'mobile_user',
      'display_name': 'Mobile User',
    }));
  }

  void disconnect() {
    _channel?.sink.close();
  }

  void sendMessage(String roomId, String content) {
    _channel?.sink.add(json.encode({
      'type': 'send_message',
      'room_id': roomId,
      'content': content,
    }));
  }

  Stream<dynamic> get messages => _channel!.stream.map((data) => json.decode(data));
}
