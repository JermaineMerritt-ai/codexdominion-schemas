'use client';

import React from 'react';
import HomeLayout from '@/components/home/HomeLayout';
import IdentityHeader from '@/components/home/IdentityHeader';
import CurrentStoryCard from '@/components/home/CurrentStoryCard';
import CurrentMissionCard from '@/components/home/CurrentMissionCard';
import CurrentCurriculumCard from '@/components/home/CurrentCurriculumCard';
import MyCircleCard from '@/components/home/MyCircleCard';
import MyProgressCard from '@/components/home/MyProgressCard';
import AdminOverviewCard from '@/components/home/AdminOverviewCard';
import {
  useCurrentUser,
  useUserProfile,
  useCurrentSeason,
  useCurrentStory,
  useCurrentMission,
  useCurrentCurriculum,
  useUserCircles,
  useAnalyticsOverview,
} from '@/lib/hooks/useHomeData';

export default function HomePage() {
  // TODO: Replace with actual auth token from your auth system
  const authToken = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

  // Fetch all data
  const { user, loading: userLoading } = useCurrentUser(authToken || undefined);
  const { profile } = useUserProfile(authToken || undefined);
  const { season, loading: seasonLoading } = useCurrentSeason();
  const { story, loading: storyLoading } = useCurrentStory(authToken || undefined);
  const { mission, loading: missionLoading } = useCurrentMission(authToken || undefined);
  const { modules, loading: curriculumLoading } = useCurrentCurriculum(authToken || undefined);
  const { circles, loading: circlesLoading } = useUserCircles(authToken || undefined);
  const { analytics } = useAnalyticsOverview(authToken || undefined);

  // Calculate current week from season
  const getCurrentWeek = () => {
    if (!season?.startDate) return 1;
    const start = new Date(season.startDate);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - start.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.min(Math.ceil(diffDays / 7), 4);
  };

  // Determine user's primary role
  const getPrimaryRole = () => {
    if (!user?.roles || user.roles.length === 0) return 'YOUTH';
    const roleHierarchy = ['COUNCIL', 'ADMIN', 'REGIONAL_DIRECTOR', 'YOUTH_CAPTAIN', 'CREATOR', 'YOUTH'];
    return roleHierarchy.find((r) => user.roles.includes(r)) || 'YOUTH';
  };

  const primaryRole = getPrimaryRole();
  const isAdmin = ['ADMIN', 'REGIONAL_DIRECTOR', 'COUNCIL'].includes(primaryRole);
  const isYouthCaptain = primaryRole === 'YOUTH_CAPTAIN';
  const isYouth = primaryRole === 'YOUTH';

  // Loading state
  if (userLoading || seasonLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">🔥</div>
          <p className="text-gray-600">Loading your dominion...</p>
        </div>
      </div>
    );
  }

  // Not authenticated
  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">🔥</div>
          <p className="text-gray-600 mb-4">You must be logged in to access the Home dashboard.</p>
          <a href="/login" className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Log In
          </a>
        </div>
      </div>
    );
  }

  const currentWeek = getCurrentWeek();

  // Get primary circle (first circle user is member of)
  const primaryCircle = circles && circles.length > 0 ? circles[0] : null;

  // Header component
  const header = (
    <IdentityHeader
      userName={user.name || user.email.split('@')[0]}
      role={primaryRole as any}
      seasonName={season?.name || 'IDENTITY'}
      currentWeek={currentWeek}
    />
  );

  // Left column: Civilization Pulse
  const leftColumn = (
    <>
      {/* Current Story */}
      {story && !storyLoading ? (
        <CurrentStoryCard
          title={story.title}
          content={story.content}
          seasonName={season?.name}
          week={story.week}
        />
      ) : (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
          <p className="text-gray-500 italic">Loading story...</p>
        </div>
      )}

      {/* Current Mission */}
      {mission && !missionLoading ? (
        <CurrentMissionCard
          missionId={mission.id}
          title={mission.title}
          description={mission.description}
          status={mission.status || 'not-started'}
          dueDate={mission.dueDate}
        />
      ) : (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <p className="text-gray-500 italic">Loading mission...</p>
        </div>
      )}

      {/* Current Curriculum */}
      {!curriculumLoading ? (
        <CurrentCurriculumCard
          modules={modules || []}
          seasonName={season?.name || 'IDENTITY'}
          week={currentWeek}
        />
      ) : (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
          <p className="text-gray-500 italic">Loading curriculum...</p>
        </div>
      )}
    </>
  );

  // Right column: My Circle + Progress OR Admin Overview
  const rightColumn = isAdmin ? (
    <AdminOverviewCard
      activeYouth={analytics?.activeYouth || 0}
      activeCircles={analytics?.activeCircles || 0}
      missionsCompletedThisWeek={analytics?.missionsCompletedThisWeek || 0}
      regionsActive={analytics?.regionsActive || 0}
    />
  ) : (
    <>
      {/* My Circle */}
      {primaryCircle && !circlesLoading ? (
        <MyCircleCard
          circleId={primaryCircle.id}
          circleName={primaryCircle.name}
          role={isYouthCaptain ? 'YOUTH_CAPTAIN' : 'YOUTH'}
          nextSessionDate={primaryCircle.nextSession?.date}
          nextSessionTime={primaryCircle.nextSession?.time}
          memberCount={primaryCircle.memberCount}
          lastAttendanceRate={primaryCircle.lastAttendanceRate}
        />
      ) : (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
          <p className="text-gray-500 italic">No circle assigned</p>
        </div>
      )}

      {/* My Progress */}
      <MyProgressCard
        missionsCompletedThisSeason={profile?.missionsCompletedThisSeason || 0}
        sessionsAttendedThisMonth={profile?.sessionsAttendedThisMonth || 0}
        currentStreak={profile?.currentStreak || 0}
      />
    </>
  );

  return <HomeLayout header={header} leftColumn={leftColumn} rightColumn={rightColumn} />;
}
