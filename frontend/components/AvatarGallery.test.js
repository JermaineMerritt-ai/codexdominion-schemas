import React from 'react';
import { render, screen } from '@testing-library/react';
import AvatarGallery from './AvatarGallery.js';

describe('AvatarGallery', () => {
  test('renders all avatar titles', () => {
    const avatars = ['Flamekeeper', 'Archivist', 'Seer', 'Sentinel', 'Echoist'];
    render(<AvatarGallery />);
    avatars.forEach((title) => {
      expect(screen.getByText(new RegExp(title, 'i'))).toBeInTheDocument();
    });
  });
});
