/**
 * Main Dashboard - Identity-Aware Home Screen
 * Routes based on user identity: Youth/Creator/Legacy-Builder/Admin
 */

'use client';

import { useAuth } from '@/lib/auth/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import apiClient from '@/lib/api/client';

interface DashboardData {
  currentMission?: any;
  currentStory?: any;
  myCircles?: any[];
  currentSeason?: any;
}

export default function DashboardPage() {
  const { user, identity, isAuthenticated, isLoading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [dashboardData, setDashboardData] = useState<DashboardData>({});
  const [isLoading, setIsLoading] = useState(true);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Fetch dashboard data
  useEffect(() => {
    if (isAuthenticated) {
      Promise.all([
        apiClient.getCurrentMission().catch(() => null),
        apiClient.getCurrentStory().catch(() => null),
        apiClient.getCircles().catch(() => []),
        apiClient.getCurrentSeason().catch(() => null),
      ]).then(([mission, story, circles, season]) => {
        setDashboardData({
          currentMission: mission,
          currentStory: story,
          myCircles: circles,
          currentSeason: season,
        });
        setIsLoading(false);
      });
    }
  }, [isAuthenticated]);

  if (authLoading || !user) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#f5f5f5',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            fontSize: '48px',
            marginBottom: '16px',
          }}>🔱</div>
          <div style={{ fontSize: '18px', color: '#666' }}>Loading Empire Dashboard...</div>
        </div>
      </div>
    );
  }

  const { currentMission, currentStory, myCircles, currentSeason } = dashboardData;

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      {/* Header */}
      <header style={{
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
        color: 'white',
        padding: '20px 40px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <div>
            <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '4px' }}>
              🔱 CodexDominion Empire
            </h1>
            <p style={{ fontSize: '14px', opacity: 0.8 }}>
              {currentSeason?.name || 'Season of Identity'} • Week {currentSeason?.week || 1}
            </p>
          </div>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontWeight: '600' }}>{user.firstName} {user.lastName}</div>
              <div style={{ fontSize: '12px', opacity: 0.8 }}>
                {identity === 'ADMIN' ? '🔱 Admin' :
                 identity === 'LEGACY_BUILDER' ? '👑 Legacy-Builder' :
                 identity === 'CREATOR' ? '🎨 Creator' :
                 '🔥 Youth'}
              </div>
            </div>
            <button
              onClick={logout}
              style={{
                padding: '8px 16px',
                background: 'rgba(255,255,255,0.2)',
                border: 'none',
                borderRadius: '6px',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '40px',
      }}>
        {/* Identity Header Card */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '32px',
          marginBottom: '32px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}>
          <h2 style={{ fontSize: '28px', marginBottom: '8px' }}>
            Welcome, {user.firstName}
          </h2>
          <p style={{ fontSize: '16px', color: '#666' }}>
            {identity === 'YOUTH' && 'Your journey to mastery begins here. Complete your weekly mission and connect with your circle.'}
            {identity === 'CREATOR' && 'Your studio awaits. Build artifacts, complete challenges, and share your creations.'}
            {identity === 'LEGACY_BUILDER' && 'Guide the next generation. Oversee circles, expand regions, and uphold the culture.'}
            {identity === 'ADMIN' && 'Command center active. All nine engines operational. The civilization grows.'}
          </p>
        </div>

        {isLoading ? (
          <div style={{ textAlign: 'center', padding: '60px', color: '#999' }}>
            Loading dashboard data...
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
            {/* Current Mission Card */}
            {currentMission && (
              <div style={{
                background: 'white',
                borderRadius: '12px',
                padding: '24px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '16px',
                }}>
                  <h3 style={{ fontSize: '18px', fontWeight: '600' }}>Current Mission</h3>
                  <span style={{
                    padding: '4px 12px',
                    background: '#e8f5e9',
                    color: '#2e7d32',
                    borderRadius: '12px',
                    fontSize: '12px',
                    fontWeight: '600',
                  }}>
                    This Week
                  </span>
                </div>
                <h4 style={{ fontSize: '16px', marginBottom: '8px', color: '#333' }}>
                  {currentMission.title || 'No active mission'}
                </h4>
                <p style={{ fontSize: '14px', color: '#666', marginBottom: '16px' }}>
                  {currentMission.description || 'Check back soon for your next mission'}
                </p>
                <button style={{
                  padding: '10px 20px',
                  background: '#1a1a2e',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600',
                }}>
                  View Mission
                </button>
              </div>
            )}

            {/* Current Story Card */}
            {currentStory && (
              <div style={{
                background: 'white',
                borderRadius: '12px',
                padding: '24px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '16px',
                }}>
                  <h3 style={{ fontSize: '18px', fontWeight: '600' }}>Cultural Story</h3>
                  <span style={{ fontSize: '24px' }}>📖</span>
                </div>
                <h4 style={{ fontSize: '16px', marginBottom: '8px', color: '#333' }}>
                  {currentStory.title || 'No story this week'}
                </h4>
                <p style={{ fontSize: '14px', color: '#666', marginBottom: '16px' }}>
                  {currentStory.content?.substring(0, 120) + '...' || 'Check back soon'}
                </p>
                <button style={{
                  padding: '10px 20px',
                  background: '#fff',
                  color: '#1a1a2e',
                  border: '2px solid #1a1a2e',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600',
                }}>
                  Read Story
                </button>
              </div>
            )}

            {/* My Circles Card */}
            <div style={{
              background: 'white',
              borderRadius: '12px',
              padding: '24px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '16px',
              }}>
                <h3 style={{ fontSize: '18px', fontWeight: '600' }}>My Circles</h3>
                <span style={{ fontSize: '24px' }}>⭕</span>
              </div>
              {myCircles && myCircles.length > 0 ? (
                <div>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#1a1a2e', marginBottom: '8px' }}>
                    {myCircles.length}
                  </div>
                  <p style={{ fontSize: '14px', color: '#666', marginBottom: '16px' }}>
                    Active circles • Next session soon
                  </p>
                  <button style={{
                    padding: '10px 20px',
                    background: '#fff',
                    color: '#1a1a2e',
                    border: '2px solid #1a1a2e',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                  }}>
                    View Circles
                  </button>
                </div>
              ) : (
                <p style={{ fontSize: '14px', color: '#999' }}>
                  No circles yet. Join one to connect with your community.
                </p>
              )}
            </div>

            {/* Quick Actions Card */}
            <div style={{
              background: 'white',
              borderRadius: '12px',
              padding: '24px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}>
              <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>Quick Actions</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <button style={{
                  padding: '12px',
                  background: '#f5f5f5',
                  border: 'none',
                  borderRadius: '8px',
                  textAlign: 'left',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                }}>
                  📋 View All Missions
                </button>
                {identity === 'CREATOR' && (
                  <button style={{
                    padding: '12px',
                    background: '#f5f5f5',
                    border: 'none',
                    borderRadius: '8px',
                    textAlign: 'left',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                  }}>
                    🎨 Creator Studio
                  </button>
                )}
                {(identity === 'LEGACY_BUILDER' || identity === 'ADMIN') && (
                  <button style={{
                    padding: '12px',
                    background: '#f5f5f5',
                    border: 'none',
                    borderRadius: '8px',
                    textAlign: 'left',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                  }}>
                    📊 Analytics Overview
                  </button>
                )}
                <button style={{
                  padding: '12px',
                  background: '#f5f5f5',
                  border: 'none',
                  borderRadius: '8px',
                  textAlign: 'left',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                }}>
                  ⚙️ Settings
                </button>
              </div>
            </div>
          </div>
        )}

        {/* System Status Footer */}
        <div style={{
          marginTop: '40px',
          padding: '20px',
          background: 'white',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '12px', color: '#999' }}>
            🔥 Backend: <span style={{ color: '#2e7d32', fontWeight: '600' }}>OPERATIONAL</span> •
            Nine Engines: <span style={{ color: '#2e7d32', fontWeight: '600' }}>LIVE</span> •
            API: <span style={{ color: '#2e7d32', fontWeight: '600' }}>http://localhost:4000</span>
          </div>
        </div>
      </main>
    </div>
  );
}
