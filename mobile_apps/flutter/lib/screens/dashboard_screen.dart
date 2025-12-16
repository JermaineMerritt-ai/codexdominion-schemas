import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_client.dart';
import '../services/websocket_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
  }

  void _connectWebSocket() {
    final wsService = context.read<WebSocketService>();
    wsService.connect();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Codex Dominion'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {
              // Show notifications
            },
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              // Navigate to settings
            },
          ),
        ],
      ),
      drawer: _buildDrawer(),
      body: _buildBody(),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
        BottomNavigationBarItem(icon: Icon(Icons.share), label: 'Social'),
        BottomNavigationBarItem(icon: Icon(Icons.attach_money), label: 'Affiliate'),
        BottomNavigationBarItem(icon: Icon(Icons.chat_bubble), label: 'Chatbot'),
        BottomNavigationBarItem(icon: Icon(Icons.psychology), label: 'Algorithm')
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Quick action
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildDrawer() {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  Color(int.parse('#667eea'.substring(1), radix: 16) + 0xFF000000),
                  Color(int.parse('#764ba2'.substring(1), radix: 16) + 0xFF000000),
                ],
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const CircleAvatar(
                  radius: 30,
                  child: Icon(Icons.person, size: 40),
                ),
                const SizedBox(height: 10),
                const Text(
                  'Codex Dominion',
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const Text(
                  'All Systems Operational',
                  style: TextStyle(color: Colors.white70, fontSize: 14),
                ),
              ],
            ),
          ),
                    ListTile(
            leading: Icon(Icons.home),
            title: Text('Home'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /
            },
          ),
          ListTile(
            leading: Icon(Icons.share),
            title: Text('Social'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /social
            },
          ),
          ListTile(
            leading: Icon(Icons.attach_money),
            title: Text('Affiliate'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /affiliate
            },
          ),
          ListTile(
            leading: Icon(Icons.chat_bubble),
            title: Text('Chatbot'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /chatbot
            },
          ),
          ListTile(
            leading: Icon(Icons.psychology),
            title: Text('Algorithm'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /algorithm
            },
          ),
          ListTile(
            leading: Icon(Icons.publish),
            title: Text('Auto-Publish'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /autopublish
            },
          ),
          ListTile(
            leading: Icon(Icons.settings),
            title: Text('Engines'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /engines
            },
          ),
          ListTile(
            leading: Icon(Icons.build),
            title: Text('Tools'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /tools
            },
          ),
          ListTile(
            leading: Icon(Icons.dashboard),
            title: Text('Dashboards'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /dashboards
            },
          ),
          ListTile(
            leading: Icon(Icons.forum),
            title: Text('Chat'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /chat
            },
          ),
          ListTile(
            leading: Icon(Icons.smart_toy),
            title: Text('Agents'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /agents
            },
          ),
          ListTile(
            leading: Icon(Icons.public),
            title: Text('Websites'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /websites
            },
          ),
          ListTile(
            leading: Icon(Icons.shopping_cart),
            title: Text('Stores'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /stores
            },
          ),
          ListTile(
            leading: Icon(Icons.account_tree),
            title: Text('Workflows'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /workflows
            },
          ),
          ListTile(
            leading: Icon(Icons.health_and_safety),
            title: Text('Health'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /health
            },
          ),
          ListTile(
            leading: Icon(Icons.audiotrack),
            title: Text('Audio'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /audio
            },
          ),
          ListTile(
            leading: Icon(Icons.message),
            title: Text('💬 Chat'),
            onTap: () {
              Navigator.pop(context);
              // Navigate to /chat-ws
            },
          ),
        ],
      ),
    );
  }

  Widget _buildBody() {
    switch (_selectedIndex) {
      case 0:
        return _buildHomeTab();
      case 1:
        return _buildSocialTab();
      case 2:
        return _buildAffiliateTab();
      case 3:
        return _buildChatbotTab();
      case 4:
        return _buildAlgorithmTab();
      default:
        return const Center(child: Text('Coming Soon'));
    }
  }

  Widget _buildHomeTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        width: 12,
                        height: 12,
                        decoration: BoxDecoration(
                          color: Colors.green,
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 8),
                      const Text(
                        'System Status',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'ALL SYSTEMS OPERATIONAL',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.green,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text('17 Navigation Tabs Active'),
                  const Text('Dashboard: Running'),
                  const Text('WebSocket: Connected'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          _buildStatsGrid(),
        ],
      ),
    );
  }

  Widget _buildStatsGrid() {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 16,
      crossAxisSpacing: 16,
      children: [
        _buildStatCard('Social Followers', '57,000+', Icons.people),
        _buildStatCard('Affiliate Earnings', r'$12,694', Icons.attach_money),
        _buildStatCard('Chatbot Satisfaction', '94%', Icons.sentiment_satisfied),
        _buildStatCard('Active Workflows', '12', Icons.account_tree),
      ],
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: Theme.of(context).colorScheme.primary),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSocialTab() {
    return const Center(child: Text('Social Media Tab'));
  }

  Widget _buildAffiliateTab() {
    return const Center(child: Text('Affiliate Tab'));
  }

  Widget _buildChatbotTab() {
    return const Center(child: Text('Chatbot Tab'));
  }

  Widget _buildAlgorithmTab() {
    return const Center(child: Text('Algorithm Tab'));
  }
}
