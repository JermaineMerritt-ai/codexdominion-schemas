"""Create demo team with sample projects for constellation testing"""
from flask_dashboard import db, app, User, Team, TeamMember, GraphicsProject
import random

app.app_context().push()

# Create or get test user
user = User.query.filter_by(email='demo@codex.ai').first()
if not user:
    user = User(email='demo@codex.ai')
    user.set_password('demo123')
    db.session.add(user)
    db.session.commit()
    print('✅ Created new demo user')
else:
    print('✅ Using existing demo user')

# Create test team
team = Team(name='Demo Creative Team', description='Testing constellation feature', owner_id=user.id)
db.session.add(team)
db.session.commit()

# Add user as team owner
member = TeamMember(team_id=team.id, user_id=user.id, role='owner')
db.session.add(member)
db.session.commit()

# Create sample projects with various tags and categories
moods = ['dramatic', 'serene', 'vibrant', 'mysterious', 'ethereal']
palettes = ['warm', 'cool', 'monochrome', 'vibrant', 'pastel']
categories = ['Character Art', 'Landscape', 'Concept Art', 'Portrait', 'Abstract']
tags_pool = ['fantasy', 'scifi', 'nature', 'urban', 'surreal', 'minimal', 'detailed', 'colorful']

for i in range(25):
    project = GraphicsProject(
        user_id=user.id,
        team_id=team.id,
        prompt=f'Test project {i+1}: A {random.choice(moods)} scene with {random.choice(tags_pool)} elements',
        mood=random.choice(moods),
        color_palette=random.choice(palettes),
        category=random.choice(categories),
        tags=', '.join(random.sample(tags_pool, k=random.randint(2, 4)))
    )
    db.session.add(project)

db.session.commit()

print('✅ Demo data created successfully!')
print(f'📧 Login: demo@codex.ai / demo123')
print(f'👑 Team ID: {team.id}')
print(f'🌠 Constellation: http://localhost:5000/studio/graphics/team/{team.id}/constellation')
print(f'📚 Team Library: http://localhost:5000/studio/graphics/team/{team.id}')
print(f'✨ AI Prompts: http://localhost:5000/studio/graphics/recommendations/{team.id}/prompts')
