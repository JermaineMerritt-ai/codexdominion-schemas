import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { RoleName, SubmissionStatus } from '@prisma/client';

@Injectable()
export class AnalyticsService {
  constructor(private prisma: PrismaService) {}

  /**
   * GET /analytics/dashboard
   * Simplified metrics for dashboard widgets
   */
  async getDashboard() {
    const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);

    const [
      activeYouth,
      activeCircles,
      missionsCompletedThisWeek,
      regionsActive,
    ] = await Promise.all([
      // Active youth (in circles with recent activity)
      this.prisma.user.count({
        where: {
          roles: { some: { role: { name: RoleName.YOUTH } } },
          circleMemberships: {
            some: {
              circle: {
                sessions: {
                  some: {
                    scheduledAt: { gte: thirtyDaysAgo }
                  }
                }
              }
            }
          }
        }
      }),

      // Active circles (sessions in last 30 days)
      this.prisma.circle.count({
        where: {
          sessions: {
            some: {
              scheduledAt: { gte: thirtyDaysAgo }
            }
          }
        }
      }),

      // Missions completed this week
      this.prisma.missionSubmission.count({
        where: {
          status: SubmissionStatus.APPROVED,
          submittedAt: { gte: oneWeekAgo }
        }
      }),

      // Regions with activity in last 30 days
      this.prisma.region.count({
        where: {
          circles: {
            some: {
              sessions: {
                some: {
                  scheduledAt: { gte: thirtyDaysAgo }
                }
              }
            }
          }
        }
      }),
    ]);

    return {
      active_youth: activeYouth,
      active_circles: activeCircles,
      missions_completed_this_week: missionsCompletedThisWeek,
      regions_active: regionsActive,
    };
  }

  /**
   * GET /analytics/overview
   * Core metrics for Empire Dashboard
   */
  async getOverview() {
    const [
      // User metrics
      totalUsers,
      activeYouth,
      youthCaptains,
      ambassadors,
      regionalDirectors,
      
      // Circle metrics
      totalCircles,
      activeCircles,
      avgCircleSize,
      
      // Mission metrics
      totalMissions,
      completedSubmissions,
      
      // Event metrics
      totalEvents,
      upcomingEvents,
      
      // Creator metrics
      totalArtifacts,
      
      // Region metrics
      totalRegions,
      totalSchools,
      
      // Season context
      currentSeason,
    ] = await Promise.all([
      // User counts by role
      this.prisma.user.count(),
      this.prisma.userRole.count({ where: { role: { name: RoleName.YOUTH } } }),
      this.prisma.userRole.count({ where: { role: { name: RoleName.YOUTH_CAPTAIN } } }),
      this.prisma.userRole.count({ where: { role: { name: RoleName.AMBASSADOR } } }),
      this.prisma.userRole.count({ where: { role: { name: RoleName.REGIONAL_DIRECTOR } } }),
      
      // Circle metrics
      this.prisma.circle.count(),
      this.prisma.circle.count({ 
        where: { 
          sessions: { 
            some: { 
              scheduledAt: { gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } 
            } 
          } 
        } 
      }),
      this.prisma.circleMember.groupBy({ by: ['circleId'], _count: { userId: true } })
        .then(groups => {
          if (groups.length === 0) return 0;
          const total = groups.reduce((sum, g) => sum + g._count.userId, 0);
          return Math.round(total / groups.length);
        }),
      
      // Mission metrics
      this.prisma.mission.count(),
      this.prisma.missionSubmission.count({ where: { status: SubmissionStatus.APPROVED } }),
      
      // Event metrics
      this.prisma.event.count(),
      this.prisma.event.count({ where: { scheduledAt: { gte: new Date() } } }),
      
      // Creator metrics
      this.prisma.artifact.count(),
      
      // Region metrics
      this.prisma.region.count(),
      this.prisma.school.count(),
      
      // Season context
      this.prisma.season.findFirst({ 
        where: { 
          startDate: { lte: new Date() },
          endDate: { gte: new Date() }
        },
        orderBy: { startDate: 'desc' }
      }),
    ]);

    return {
      // High-level KPIs
      users: {
        total: totalUsers,
        youth: activeYouth,
        captains: youthCaptains,
        ambassadors,
        regionalDirectors,
      },
      
      circles: {
        total: totalCircles,
        active: activeCircles,
        avgSize: avgCircleSize,
      },
      
      missions: {
        total: totalMissions,
        completedApproved: completedSubmissions,
      },
      
      events: {
        total: totalEvents,
        upcoming: upcomingEvents,
      },
      
      creators: {
        artifacts: totalArtifacts,
      },
      
      expansion: {
        regions: totalRegions,
        schools: totalSchools,
      },
      
      season: {
        current: currentSeason?.name || 'IDENTITY',
        startDate: currentSeason?.startDate,
        endDate: currentSeason?.endDate,
      },
      
      message: 'Empire Dashboard metrics loaded successfully',
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * GET /analytics/circles?region_id=...
   * Detailed circle health metrics (filterable by region)
   */
  async getCircleMetrics(regionId?: string) {
    const circles = await this.prisma.circle.findMany({
      where: regionId ? { regionId } : undefined,
      include: {
        captain: {
          include: {
            circleMemberships: {
              where: { circleId: { not: undefined } },
              take: 1,
            }
          }
        },
        members: { 
          include: { 
            user: { 
              select: { 
                id: true, 
                firstName: true, 
                lastName: true,
                roles: { include: { role: true } }
              } 
            } 
          } 
        },
        sessions: {
          include: {
            attendance: true,
          },
          orderBy: { scheduledAt: 'desc' },
          take: 10,
        },
        region: true,
      },
    });

    return circles.map(circle => {
      const totalSessions = circle.sessions.length;
      const recentSessions = circle.sessions.filter(s => 
        s.scheduledAt > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      ).length;
      
      const totalAttendance = circle.sessions.reduce((sum, s) => sum + s.attendance.length, 0);
      const avgAttendance = totalSessions > 0 ? Math.round(totalAttendance / totalSessions) : 0;

      // Calculate session frequency (sessions per month)
      const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
      const sessionsLastMonth = circle.sessions.filter(s => s.scheduledAt >= thirtyDaysAgo).length;

      // Calculate captain activity (last session facilitated)
      const lastSession = circle.sessions[0]; // Already ordered by scheduledAt desc
      const captainLastActive = lastSession ? lastSession.scheduledAt : null;
      const captainActiveDays = captainLastActive 
        ? Math.floor((Date.now() - captainLastActive.getTime()) / (1000 * 60 * 60 * 24))
        : null;

      // Calculate youth participation rate
      const youthMembers = circle.members.filter(m => 
        m.user.roles.some(ur => ur.role.name === RoleName.YOUTH)
      );
      const youthCount = youthMembers.length;
      
      // Count unique youth who attended at least one session
      const youthAttendees = new Set<string>();
      circle.sessions.forEach(session => {
        session.attendance.forEach(att => {
          if (youthMembers.some(ym => ym.userId === att.userId)) {
            youthAttendees.add(att.userId);
          }
        });
      });
      
      const youthParticipationRate = youthCount > 0 
        ? Math.round((youthAttendees.size / youthCount) * 100)
        : 0;

      return {
        id: circle.id,
        name: circle.name,
        region: circle.region?.name,
        numberOfCircles: 1, // This is a single circle
        members: circle.members.length,
        youthMembers: youthCount,
        sessions: {
          total: totalSessions,
          recent: recentSessions,
          avgAttendance,
          frequencyPerMonth: sessionsLastMonth,
        },
        captainActivity: {
          captainName: circle.captain ? `${circle.captain.firstName} ${circle.captain.lastName}` : 'Unassigned',
          lastActive: captainLastActive,
          activeDaysAgo: captainActiveDays,
          status: captainActiveDays === null ? 'inactive' : captainActiveDays < 14 ? 'active' : captainActiveDays < 30 ? 'moderate' : 'low',
        },
        youthParticipationRate,
        health: recentSessions >= 2 ? 'healthy' : recentSessions >= 1 ? 'moderate' : 'inactive',
      };
    });
  }

  /**
   * GET /analytics/missions?region_id=...
   * Mission completion and engagement metrics (filterable by region)
   */
  async getMissionMetrics(regionId?: string) {
    // Build where clause for region filtering
    const missionWhere = regionId ? {
      OR: [
        { regionId }, // Regional missions
        { type: 'REGIONAL' as const }, // Include regional type missions
      ]
    } : undefined;

    const missions = await this.prisma.mission.findMany({
      where: missionWhere,
      include: {
        season: true,
        assignments: {
          include: {
            circle: { select: { id: true, name: true, regionId: true } }
          }
        },
        submissions: {
          include: {
            assignment: {
              include: {
                circle: { select: { id: true, name: true, regionId: true } }
              }
            }
          }
        },
      },
    });

    // Calculate top circles and regions by mission completion
    const circleCompletions: Record<string, { name: string; count: number }> = {};
    const regionCompletions: Record<string, number> = {};

    missions.forEach(mission => {
      mission.submissions
        .filter(s => s.status === SubmissionStatus.APPROVED)
        .forEach(submission => {
          const circle = submission.assignment?.circle;
          if (circle) {
            // Track circle completions
            if (!circleCompletions[circle.id]) {
              circleCompletions[circle.id] = { name: circle.name, count: 0 };
            }
            circleCompletions[circle.id].count++;

            // Track region completions
            if (circle.regionId) {
              regionCompletions[circle.regionId] = (regionCompletions[circle.regionId] || 0) + 1;
            }
          }
        });
    });

    // Get top 5 circles and regions
    const topCircles = Object.entries(circleCompletions)
      .sort(([, a], [, b]) => b.count - a.count)
      .slice(0, 5)
      .map(([id, data]) => ({ circleId: id, name: data.name, completions: data.count }));

    const topRegions = Object.entries(regionCompletions)
      .sort(([, a], [, b]) => (b as number) - (a as number))
      .slice(0, 5)
      .map(([regionId, count]) => ({ regionId, completions: count }));

    return {
      missions: missions.map(mission => {
        const approvedSubmissions = mission.submissions.filter(s => s.status === SubmissionStatus.APPROVED).length;
        const completionRate = mission.assignments.length > 0 
          ? Math.round((approvedSubmissions / mission.assignments.length) * 100)
          : 0;

        return {
          id: mission.id,
          title: mission.title,
          season: mission.season.name,
          type: mission.type,
          assigned: mission.assignments.length,
          submitted: mission.submissions.length,
          approved: approvedSubmissions,
          completionRate,
        };
      }),
      topCircles,
      topRegions,
    };
  }

  /**
   * GET /analytics/regions
   * Regional expansion and activity metrics (Regional Director's cockpit)
   */
  async getRegionMetrics() {
    const regions = await this.prisma.region.findMany({
      include: {
        circles: {
          include: {
            members: {
              include: {
                user: {
                  include: {
                    roles: { include: { role: true } }
                  }
                }
              }
            },
            sessions: {
              where: {
                scheduledAt: { gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
              }
            }
          }
        },
        schools: true,
        events: {
          where: {
            scheduledAt: { gte: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000) }
          }
        },
        outreach: true,
      },
    });

    // Get mission completions per region
    const missionCompletions = await this.prisma.missionSubmission.findMany({
      where: {
        status: SubmissionStatus.APPROVED,
      },
      include: {
        assignment: {
          include: {
            circle: {
              select: { regionId: true }
            }
          }
        }
      }
    });

    // Map region IDs to mission completion counts
    const regionMissionCounts: Record<string, number> = {};
    missionCompletions.forEach(submission => {
      const regionId = submission.assignment?.circle?.regionId;
      if (regionId) {
        regionMissionCounts[regionId] = (regionMissionCounts[regionId] || 0) + 1;
      }
    });

    return regions.map(region => {
      const totalMembers = region.circles.reduce((sum, c) => sum + c.members.length, 0);
      
      // Count youth in this region
      const youthInRegion = region.circles.reduce((sum, circle) => {
        const youthCount = circle.members.filter(member =>
          member.user.roles.some(ur => ur.role.name === RoleName.YOUTH)
        ).length;
        return sum + youthCount;
      }, 0);

      const recentSessions = region.circles.reduce((sum, c) => sum + c.sessions.length, 0);
      const missionsCompleted = regionMissionCounts[region.id] || 0;

      return {
        id: region.id,
        name: region.name,
        country: region.country,
        youthPerRegion: youthInRegion,
        circlesPerRegion: region.circles.length,
        schools: region.schools.length,
        totalMembers,
        missionCompletionPerRegion: missionsCompleted,
        recentSessions,
        events: region.events.length,
        outreachEventsPerRegion: region.outreach.length,
        activity: recentSessions >= 4 ? 'high' : recentSessions >= 2 ? 'moderate' : 'low',
      };
    });
  }

  /**
   * GET /analytics/creators
   * Creator output and challenge metrics
   */
  async getCreatorMetrics() {
    const [
      totalCreators,
      artifacts,
      challenges,
      recentSubmissions,
    ] = await Promise.all([
      this.prisma.userRole.count({ where: { role: { name: RoleName.CREATOR } } }),
      this.prisma.artifact.findMany({
        include: {
          creator: { select: { id: true, email: true, firstName: true, lastName: true } },
        },
        orderBy: { createdAt: 'desc' },
        take: 50,
      }),
      this.prisma.creatorChallenge.findMany({
        include: {
          season: true,
          submissions: true,
        },
      }),
      this.prisma.artifact.count({
        where: {
          createdAt: { gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
        }
      }),
    ]);

    const artifactsByType = artifacts.reduce((acc, a) => {
      acc[a.artifactType] = (acc[a.artifactType] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const challengeMetrics = challenges.map(challenge => ({
      id: challenge.id,
      title: challenge.title,
      season: challenge.season?.name,
      submissions: challenge.submissions.length,
      deadline: challenge.deadline,
    }));

    return {
      totalCreators,
      totalArtifacts: artifacts.length,
      recentSubmissions,
      artifactsByType,
      challenges: challengeMetrics,
      topCreators: this.getTopCreators(artifacts),
    };
  }

  /**
   * GET /analytics/youth
   * Youth engagement and progression metrics
   */
  async getYouthMetrics() {
    const youth = await this.prisma.user.findMany({
      where: { roles: { some: { role: { name: RoleName.YOUTH } } } },
      include: {
        profile: true,
        circleMemberships: {
          include: {
            circle: true,
          }
        },
        missionAssignments: {
          include: {
            submissions: true,
          }
        },
      },
    });

    const byRisePath = youth.reduce((acc, y) => {
      const path = y.profile?.risePath || 'IDENTITY';
      acc[path] = (acc[path] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const inCircles = youth.filter(y => y.circleMemberships.length > 0).length;
    const withMissions = youth.filter(y => y.missionAssignments.length > 0).length;
    const completedMissions = youth.filter(y => 
      y.missionAssignments.some(a => a.submissions.some(s => s.status === SubmissionStatus.APPROVED))
    ).length;

    return {
      total: youth.length,
      inCircles,
      withMissions,
      completedMissions,
      byRisePath,
      engagementRate: youth.length > 0 ? Math.round((inCircles / youth.length) * 100) : 0,
    };
  }

  /**
   * GET /analytics/events
   * Event attendance and engagement metrics
   */
  async getEventMetrics() {
    const events = await this.prisma.event.findMany({
      include: {
        region: true,
        attendance: true,
        script: true,
      },
      orderBy: { scheduledAt: 'desc' },
    });

    return events.map(event => {
      const registered = event.attendance.filter(a => a.status === 'REGISTERED').length;
      const present = event.attendance.filter(a => a.status === 'PRESENT').length;
      const attendanceRate = registered > 0 ? Math.round((present / registered) * 100) : 0;

      return {
        id: event.id,
        title: event.title,
        eventType: event.eventType,
        region: event.region?.name,
        scheduledAt: event.scheduledAt,
        registered,
        present,
        attendanceRate,
        hasScript: !!event.script,
      };
    });
  }

  // Helper methods
  private getTopCreators(artifacts: any[]) {
    const creatorCounts = artifacts.reduce((acc, a) => {
      const email = a.creator.email;
      acc[email] = (acc[email] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return Object.entries(creatorCounts)
      .sort(([, a], [, b]) => (b as number) - (a as number))
      .slice(0, 10)
      .map(([email, count]) => ({ email, artifacts: count }));
  }
}
