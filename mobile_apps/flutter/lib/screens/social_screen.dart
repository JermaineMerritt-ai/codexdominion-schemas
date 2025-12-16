import 'package:flutter/material.dart';

class SocialMediaScreen extends StatelessWidget {
  const SocialMediaScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Social Media'),
      ),
      body: Center(
        child: Text('Social Media Content Here'),
      ),
    );
  }
}
