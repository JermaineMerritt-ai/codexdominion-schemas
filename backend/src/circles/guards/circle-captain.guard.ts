import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class CircleCaptainGuard implements CanActivate {
  constructor(private prisma: PrismaService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    const circleId = request.params.id;

    if (!user || !circleId) {
      throw new ForbiddenException({
        code: 'FORBIDDEN',
        message: 'Not circle captain',
      });
    }

    // Check if user is the captain of this circle
    const circle = await this.prisma.circle.findUnique({
      where: { id: circleId },
      select: { captainId: true },
    });

    if (!circle || circle.captainId !== user.id) {
      throw new ForbiddenException({
        code: 'FORBIDDEN',
        message: 'Not circle captain',
      });
    }

    return true;
  }
}
