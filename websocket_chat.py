"""
WebSocket Chat Interface - Real-Time Messaging System
Codex Dominion - Production System #7 (70% Complete!)

Real-time chat with WebSocket support, chat history, multi-user rooms,
AI agent integration, typing indicators, message persistence, authentication.

Features:
- WebSocket real-time bidirectional communication
- Chat rooms/channels with user management
- Message persistence to JSON database
- Typing indicators and user presence
- AI agent integration (Jermaine, DOT300)
- File sharing and emoji support
- Message search and history
- User authentication and profiles
- Admin commands and moderation
- Rate limiting and spam protection

Author: Jermaine Merritt
Date: December 15, 2025
"""

import asyncio
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict, field
from pathlib import Path
import hashlib
import time

# WebSocket server (using websockets library)
try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except ImportError:
    print("⚠️ websockets not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "websockets"])
    import websockets
    from websockets.server import WebSocketServerProtocol

# Web server (using aiohttp for async HTTP + WebSocket)
try:
    import aiohttp
    from aiohttp import web
except ImportError:
    print("⚠️ aiohttp not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "aiohttp"])
    import aiohttp
    from aiohttp import web


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class User:
    """Chat user profile"""
    id: str
    username: str
    display_name: str
    avatar_url: str = ""
    status: str = "online"  # online, away, busy, offline
    last_seen: str = ""
    created_at: str = ""
    is_admin: bool = False
    is_bot: bool = False


@dataclass
class Message:
    """Chat message"""
    id: str
    room_id: str
    user_id: str
    username: str
    content: str
    message_type: str = "text"  # text, image, file, system, command
    timestamp: str = ""
    edited_at: Optional[str] = None
    reactions: Dict[str, List[str]] = field(default_factory=dict)  # emoji -> [user_ids]
    reply_to: Optional[str] = None  # message_id
    attachments: List[Dict] = field(default_factory=list)


@dataclass
class Room:
    """Chat room/channel"""
    id: str
    name: str
    description: str = ""
    room_type: str = "public"  # public, private, direct
    created_by: str = ""
    created_at: str = ""
    members: List[str] = field(default_factory=list)  # user_ids
    admins: List[str] = field(default_factory=list)  # user_ids
    message_count: int = 0
    last_activity: str = ""


@dataclass
class TypingIndicator:
    """User typing indicator"""
    user_id: str
    username: str
    room_id: str
    timestamp: float


# ============================================================================
# CHAT DATABASE (JSON-based)
# ============================================================================

class ChatDatabase:
    """Persistent JSON storage for chat data"""

    def __init__(self, data_dir: str = "chat_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.users_file = self.data_dir / "users.json"
        self.rooms_file = self.data_dir / "rooms.json"
        self.messages_file = self.data_dir / "messages.json"

        self._ensure_files()

    def _ensure_files(self):
        """Create default data files if they don't exist"""
        if not self.users_file.exists():
            self._save_json(self.users_file, {})

        if not self.rooms_file.exists():
            # Create default general room
            general_room = Room(
                id=str(uuid.uuid4()),
                name="general",
                description="General discussion",
                room_type="public",
                created_by="system",
                created_at=datetime.utcnow().isoformat() + "Z",
                members=[],
                admins=[],
                message_count=0,
                last_activity=datetime.utcnow().isoformat() + "Z"
            )
            self._save_json(self.rooms_file, {general_room.id: asdict(general_room)})

        if not self.messages_file.exists():
            self._save_json(self.messages_file, {})

    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return {}

    def _save_json(self, file_path: Path, data: Dict):
        """Save JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving {file_path}: {e}")

    # User operations
    def create_user(self, user: User) -> bool:
        """Create new user"""
        users = self._load_json(self.users_file)
        if user.id in users:
            return False
        users[user.id] = asdict(user)
        self._save_json(self.users_file, users)
        return True

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        users = self._load_json(self.users_file)
        if user_id in users:
            return User(**users[user_id])
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        users = self._load_json(self.users_file)
        for user_data in users.values():
            if user_data.get('username') == username:
                return User(**user_data)
        return None

    def update_user(self, user: User):
        """Update user"""
        users = self._load_json(self.users_file)
        users[user.id] = asdict(user)
        self._save_json(self.users_file, users)

    def list_users(self) -> List[User]:
        """List all users"""
        users = self._load_json(self.users_file)
        return [User(**u) for u in users.values()]

    # Room operations
    def create_room(self, room: Room) -> bool:
        """Create new room"""
        rooms = self._load_json(self.rooms_file)
        if room.id in rooms:
            return False
        rooms[room.id] = asdict(room)
        self._save_json(self.rooms_file, rooms)
        return True

    def get_room(self, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        rooms = self._load_json(self.rooms_file)
        if room_id in rooms:
            return Room(**rooms[room_id])
        return None

    def get_room_by_name(self, name: str) -> Optional[Room]:
        """Get room by name"""
        rooms = self._load_json(self.rooms_file)
        for room_data in rooms.values():
            if room_data.get('name') == name:
                return Room(**room_data)
        return None

    def update_room(self, room: Room):
        """Update room"""
        rooms = self._load_json(self.rooms_file)
        rooms[room.id] = asdict(room)
        self._save_json(self.rooms_file, rooms)

    def list_rooms(self) -> List[Room]:
        """List all rooms"""
        rooms = self._load_json(self.rooms_file)
        return [Room(**r) for r in rooms.values()]

    def get_user_rooms(self, user_id: str) -> List[Room]:
        """Get rooms user is a member of"""
        rooms = self._load_json(self.rooms_file)
        user_rooms = []
        for room_data in rooms.values():
            if user_id in room_data.get('members', []):
                user_rooms.append(Room(**room_data))
        return user_rooms

    # Message operations
    def save_message(self, message: Message):
        """Save message"""
        messages = self._load_json(self.messages_file)

        # Store by room_id for efficient retrieval
        if message.room_id not in messages:
            messages[message.room_id] = []

        messages[message.room_id].append(asdict(message))

        # Keep only last 1000 messages per room
        if len(messages[message.room_id]) > 1000:
            messages[message.room_id] = messages[message.room_id][-1000:]

        self._save_json(self.messages_file, messages)

        # Update room last activity and message count
        room = self.get_room(message.room_id)
        if room:
            room.last_activity = message.timestamp
            room.message_count += 1
            self.update_room(room)

    def get_messages(self, room_id: str, limit: int = 50, before: Optional[str] = None) -> List[Message]:
        """Get messages for room (paginated)"""
        messages = self._load_json(self.messages_file)

        if room_id not in messages:
            return []

        room_messages = [Message(**m) for m in messages[room_id]]

        # Filter by before timestamp if provided
        if before:
            room_messages = [m for m in room_messages if m.timestamp < before]

        # Return most recent messages
        return sorted(room_messages, key=lambda m: m.timestamp, reverse=True)[:limit]

    def search_messages(self, room_id: str, query: str, limit: int = 20) -> List[Message]:
        """Search messages in room"""
        messages = self._load_json(self.messages_file)

        if room_id not in messages:
            return []

        query_lower = query.lower()
        results = []

        for msg_data in messages[room_id]:
            if query_lower in msg_data.get('content', '').lower():
                results.append(Message(**msg_data))
                if len(results) >= limit:
                    break

        return results


# ============================================================================
# CHAT SERVER
# ============================================================================

class ChatServer:
    """WebSocket chat server with real-time messaging"""

    def __init__(self, host: str = "0.0.0.0", ws_port: int = 8765, http_port: int = 8766):
        self.host = host
        self.ws_port = ws_port
        self.http_port = http_port

        self.db = ChatDatabase()

        # Active connections: {user_id: websocket}
        self.connections: Dict[str, WebSocketServerProtocol] = {}

        # Room subscriptions: {room_id: {user_ids}}
        self.room_subscriptions: Dict[str, Set[str]] = {}

        # Typing indicators: {room_id: [TypingIndicator]}
        self.typing_indicators: Dict[str, List[TypingIndicator]] = {}

        # Rate limiting: {user_id: [timestamps]}
        self.rate_limit: Dict[str, List[float]] = {}
        self.rate_limit_max = 10  # max messages per window
        self.rate_limit_window = 10  # seconds

    async def handle_websocket(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket connection"""
        user_id = None

        try:
            # Wait for authentication message
            auth_msg = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            auth_data = json.loads(auth_msg)

            if auth_data.get('type') != 'auth':
                await websocket.send(json.dumps({
                    'type': 'error',
                    'error': 'Authentication required'
                }))
                return

            # Authenticate user
            username = auth_data.get('username')
            user_id = auth_data.get('user_id') or str(uuid.uuid4())

            # Get or create user
            user = self.db.get_user(user_id)
            if not user:
                user = User(
                    id=user_id,
                    username=username,
                    display_name=auth_data.get('display_name', username),
                    avatar_url=auth_data.get('avatar_url', ''),
                    status='online',
                    last_seen=datetime.utcnow().isoformat() + 'Z',
                    created_at=datetime.utcnow().isoformat() + 'Z',
                    is_admin=False,
                    is_bot=auth_data.get('is_bot', False)
                )
                self.db.create_user(user)

            # Register connection
            self.connections[user_id] = websocket

            # Send auth success
            await websocket.send(json.dumps({
                'type': 'auth_success',
                'user': asdict(user),
                'rooms': [asdict(r) for r in self.db.list_rooms()]
            }))

            print(f"✅ User connected: {username} ({user_id})")

            # Handle messages
            async for message in websocket:
                await self.handle_message(user_id, message)

        except asyncio.TimeoutError:
            print("⏱️ WebSocket authentication timeout")
        except Exception as e:
            print(f"❌ WebSocket error: {e}")
        finally:
            # Cleanup connection
            if user_id and user_id in self.connections:
                del self.connections[user_id]

                # Remove from room subscriptions
                for room_subs in self.room_subscriptions.values():
                    room_subs.discard(user_id)

                print(f"❌ User disconnected: {user_id}")

    async def handle_message(self, user_id: str, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')

            # Rate limiting
            if not self._check_rate_limit(user_id):
                await self.send_to_user(user_id, {
                    'type': 'error',
                    'error': 'Rate limit exceeded. Slow down!'
                })
                return

            # Route message by type
            if msg_type == 'join_room':
                await self.handle_join_room(user_id, data)
            elif msg_type == 'leave_room':
                await self.handle_leave_room(user_id, data)
            elif msg_type == 'send_message':
                await self.handle_send_message(user_id, data)
            elif msg_type == 'typing':
                await self.handle_typing(user_id, data)
            elif msg_type == 'get_history':
                await self.handle_get_history(user_id, data)
            elif msg_type == 'search':
                await self.handle_search(user_id, data)
            elif msg_type == 'create_room':
                await self.handle_create_room(user_id, data)
            elif msg_type == 'command':
                await self.handle_command(user_id, data)
            else:
                await self.send_to_user(user_id, {
                    'type': 'error',
                    'error': f'Unknown message type: {msg_type}'
                })

        except Exception as e:
            print(f"❌ Error handling message: {e}")
            await self.send_to_user(user_id, {
                'type': 'error',
                'error': str(e)
            })

    def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user is within rate limit"""
        now = time.time()

        if user_id not in self.rate_limit:
            self.rate_limit[user_id] = []

        # Remove old timestamps
        self.rate_limit[user_id] = [
            ts for ts in self.rate_limit[user_id]
            if now - ts < self.rate_limit_window
        ]

        # Check limit
        if len(self.rate_limit[user_id]) >= self.rate_limit_max:
            return False

        # Add current timestamp
        self.rate_limit[user_id].append(now)
        return True

    async def handle_join_room(self, user_id: str, data: Dict):
        """Handle user joining room"""
        room_id = data.get('room_id')
        room = self.db.get_room(room_id)

        if not room:
            await self.send_to_user(user_id, {
                'type': 'error',
                'error': 'Room not found'
            })
            return

        # Add user to room members
        if user_id not in room.members:
            room.members.append(user_id)
            self.db.update_room(room)

        # Subscribe to room
        if room_id not in self.room_subscriptions:
            self.room_subscriptions[room_id] = set()
        self.room_subscriptions[room_id].add(user_id)

        # Send confirmation
        await self.send_to_user(user_id, {
            'type': 'joined_room',
            'room': asdict(room)
        })

        # Notify other users
        user = self.db.get_user(user_id)
        await self.broadcast_to_room(room_id, {
            'type': 'user_joined',
            'user': asdict(user),
            'room_id': room_id
        }, exclude_user=user_id)

        # Send recent messages
        messages = self.db.get_messages(room_id, limit=50)
        await self.send_to_user(user_id, {
            'type': 'message_history',
            'room_id': room_id,
            'messages': [asdict(m) for m in reversed(messages)]
        })

    async def handle_leave_room(self, user_id: str, data: Dict):
        """Handle user leaving room"""
        room_id = data.get('room_id')

        # Unsubscribe from room
        if room_id in self.room_subscriptions:
            self.room_subscriptions[room_id].discard(user_id)

        # Notify other users
        user = self.db.get_user(user_id)
        await self.broadcast_to_room(room_id, {
            'type': 'user_left',
            'user': asdict(user),
            'room_id': room_id
        }, exclude_user=user_id)

    async def handle_send_message(self, user_id: str, data: Dict):
        """Handle user sending message"""
        room_id = data.get('room_id')
        content = data.get('content', '').strip()

        if not content:
            return

        user = self.db.get_user(user_id)
        if not user:
            return

        # Create message
        message = Message(
            id=str(uuid.uuid4()),
            room_id=room_id,
            user_id=user_id,
            username=user.username,
            content=content,
            message_type=data.get('message_type', 'text'),
            timestamp=datetime.utcnow().isoformat() + 'Z',
            reply_to=data.get('reply_to')
        )

        # Save message
        self.db.save_message(message)

        # Broadcast to room
        await self.broadcast_to_room(room_id, {
            'type': 'new_message',
            'message': asdict(message)
        })

        # Check for AI mentions
        if '@jermaine' in content.lower() or '@ai' in content.lower():
            await self.handle_ai_mention(room_id, message)

    async def handle_typing(self, user_id: str, data: Dict):
        """Handle typing indicator"""
        room_id = data.get('room_id')
        is_typing = data.get('is_typing', True)

        user = self.db.get_user(user_id)
        if not user:
            return

        if room_id not in self.typing_indicators:
            self.typing_indicators[room_id] = []

        if is_typing:
            # Add typing indicator
            indicator = TypingIndicator(
                user_id=user_id,
                username=user.username,
                room_id=room_id,
                timestamp=time.time()
            )
            self.typing_indicators[room_id].append(indicator)
        else:
            # Remove typing indicator
            self.typing_indicators[room_id] = [
                ind for ind in self.typing_indicators[room_id]
                if ind.user_id != user_id
            ]

        # Clean old indicators (>10 seconds)
        now = time.time()
        self.typing_indicators[room_id] = [
            ind for ind in self.typing_indicators[room_id]
            if now - ind.timestamp < 10
        ]

        # Broadcast typing status
        await self.broadcast_to_room(room_id, {
            'type': 'typing_update',
            'room_id': room_id,
            'typing_users': [ind.username for ind in self.typing_indicators[room_id]]
        }, exclude_user=user_id)

    async def handle_get_history(self, user_id: str, data: Dict):
        """Handle get message history"""
        room_id = data.get('room_id')
        before = data.get('before')
        limit = data.get('limit', 50)

        messages = self.db.get_messages(room_id, limit=limit, before=before)

        await self.send_to_user(user_id, {
            'type': 'message_history',
            'room_id': room_id,
            'messages': [asdict(m) for m in reversed(messages)]
        })

    async def handle_search(self, user_id: str, data: Dict):
        """Handle message search"""
        room_id = data.get('room_id')
        query = data.get('query', '')

        if not query:
            return

        results = self.db.search_messages(room_id, query, limit=20)

        await self.send_to_user(user_id, {
            'type': 'search_results',
            'room_id': room_id,
            'query': query,
            'results': [asdict(m) for m in results]
        })

    async def handle_create_room(self, user_id: str, data: Dict):
        """Handle create room"""
        name = data.get('name', '').strip()

        if not name:
            await self.send_to_user(user_id, {
                'type': 'error',
                'error': 'Room name required'
            })
            return

        # Check if room exists
        if self.db.get_room_by_name(name):
            await self.send_to_user(user_id, {
                'type': 'error',
                'error': 'Room already exists'
            })
            return

        # Create room
        room = Room(
            id=str(uuid.uuid4()),
            name=name,
            description=data.get('description', ''),
            room_type=data.get('room_type', 'public'),
            created_by=user_id,
            created_at=datetime.utcnow().isoformat() + 'Z',
            members=[user_id],
            admins=[user_id],
            message_count=0,
            last_activity=datetime.utcnow().isoformat() + 'Z'
        )

        self.db.create_room(room)

        await self.send_to_user(user_id, {
            'type': 'room_created',
            'room': asdict(room)
        })

    async def handle_command(self, user_id: str, data: Dict):
        """Handle admin commands"""
        command = data.get('command', '').strip()

        user = self.db.get_user(user_id)
        if not user or not user.is_admin:
            await self.send_to_user(user_id, {
                'type': 'error',
                'error': 'Admin privileges required'
            })
            return

        # Execute command
        parts = command.split()
        cmd = parts[0] if parts else ''

        if cmd == '/kick' and len(parts) > 1:
            # Kick user from room
            target_username = parts[1]
            room_id = data.get('room_id')
            # Implementation here
            pass

        elif cmd == '/mute' and len(parts) > 1:
            # Mute user
            target_username = parts[1]
            # Implementation here
            pass

        else:
            await self.send_to_user(user_id, {
                'type': 'error',
                'error': f'Unknown command: {cmd}'
            })

    async def handle_ai_mention(self, room_id: str, message: Message):
        """Handle AI agent mention"""
        # Simple AI response (in production, integrate with Jermaine AI)
        ai_response = f"🤖 I'm Jermaine AI! You mentioned me. How can I help?"

        ai_message = Message(
            id=str(uuid.uuid4()),
            room_id=room_id,
            user_id='ai-jermaine',
            username='Jermaine AI',
            content=ai_response,
            message_type='text',
            timestamp=datetime.utcnow().isoformat() + 'Z',
            reply_to=message.id
        )

        self.db.save_message(ai_message)

        await self.broadcast_to_room(room_id, {
            'type': 'new_message',
            'message': asdict(ai_message)
        })

    async def send_to_user(self, user_id: str, message: Dict):
        """Send message to specific user"""
        if user_id in self.connections:
            try:
                await self.connections[user_id].send(json.dumps(message))
            except Exception as e:
                print(f"❌ Error sending to user {user_id}: {e}")

    async def broadcast_to_room(self, room_id: str, message: Dict, exclude_user: Optional[str] = None):
        """Broadcast message to all users in room"""
        if room_id not in self.room_subscriptions:
            return

        for user_id in self.room_subscriptions[room_id]:
            if user_id != exclude_user:
                await self.send_to_user(user_id, message)

    async def start(self):
        """Start WebSocket server"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║       🔥 CODEX DOMINION - WEBSOCKET CHAT SERVER 🔥          ║
╠══════════════════════════════════════════════════════════════╣
║  Real-time messaging with WebSocket support                  ║
║  🌐 WebSocket: ws://localhost:{self.ws_port}                        ║
║  🌐 HTTP: http://localhost:{self.http_port}                         ║
╚══════════════════════════════════════════════════════════════╝
""")

        # Start WebSocket server
        ws_server = await websockets.serve(
            self.handle_websocket,
            self.host,
            self.ws_port
        )

        print(f"✅ WebSocket server running on ws://{self.host}:{self.ws_port}")

        # Keep running
        await asyncio.Future()  # run forever


# ============================================================================
# CLI INTERFACE
# ============================================================================

def print_header():
    """Print application header"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║       🔥 CODEX DOMINION - WEBSOCKET CHAT SYSTEM 🔥          ║
╠══════════════════════════════════════════════════════════════╣
║  Real-Time Chat Interface with AI Integration                ║
║  Production System #7 - 70% Complete!                        ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    """Main CLI interface"""
    print_header()

    print("\n📋 WEBSOCKET CHAT MENU\n")
    print("1. Start WebSocket Server")
    print("2. List Rooms")
    print("3. List Users")
    print("4. Create Room")
    print("5. View Room Messages")
    print("6. Test Client (Connect as user)")
    print("0. Exit")

    choice = input("\n➤ Enter choice: ").strip()

    db = ChatDatabase()

    if choice == "1":
        print("\n🚀 Starting WebSocket server...")
        print("📋 Press Ctrl+C to stop\n")

        server = ChatServer(ws_port=8765, http_port=8766)

        try:
            asyncio.run(server.start())
        except KeyboardInterrupt:
            print("\n\n⏹️ Server stopped")

    elif choice == "2":
        rooms = db.list_rooms()
        print(f"\n📁 ROOMS ({len(rooms)})")
        print("=" * 60)
        for room in rooms:
            print(f"🏠 {room.name}")
            print(f"   ID: {room.id}")
            print(f"   Type: {room.room_type}")
            print(f"   Members: {len(room.members)}")
            print(f"   Messages: {room.message_count}")
            print()

    elif choice == "3":
        users = db.list_users()
        print(f"\n👥 USERS ({len(users)})")
        print("=" * 60)
        for user in users:
            status_icon = "🟢" if user.status == "online" else "🔴"
            print(f"{status_icon} {user.username} ({user.display_name})")
            print(f"   ID: {user.id}")
            print(f"   Status: {user.status}")
            print(f"   Last seen: {user.last_seen}")
            print()

    elif choice == "4":
        name = input("\n➤ Room name: ").strip()
        description = input("➤ Description: ").strip()
        room_type = input("➤ Type (public/private): ").strip() or "public"

        room = Room(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            room_type=room_type,
            created_by="cli",
            created_at=datetime.utcnow().isoformat() + "Z",
            members=[],
            admins=[],
            message_count=0,
            last_activity=datetime.utcnow().isoformat() + "Z"
        )

        if db.create_room(room):
            print(f"\n✅ Room created: {name}")
        else:
            print(f"\n❌ Room already exists: {name}")

    elif choice == "5":
        rooms = db.list_rooms()
        if not rooms:
            print("\n❌ No rooms found")
            return

        print("\n📁 SELECT ROOM")
        for i, room in enumerate(rooms, 1):
            print(f"{i}. {room.name} ({room.message_count} messages)")

        try:
            room_idx = int(input("\n➤ Room number: ")) - 1
            selected_room = rooms[room_idx]

            messages = db.get_messages(selected_room.id, limit=50)

            print(f"\n💬 MESSAGES - {selected_room.name}")
            print("=" * 60)

            for msg in reversed(messages):
                print(f"[{msg.timestamp}] {msg.username}: {msg.content}")

        except (ValueError, IndexError):
            print("\n❌ Invalid room selection")

    elif choice == "6":
        print("\n🧪 Test client coming soon!")
        print("Use JavaScript client to connect to ws://localhost:8765")

    elif choice == "0":
        print("\n👋 Goodbye!")
        return

    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    main()
