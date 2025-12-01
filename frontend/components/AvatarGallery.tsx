import React from 'react';

const avatars = [
  { title: 'Flamekeeper', img: 'flamekeeper.png' },
  { title: 'Archivist', img: 'archivist.png' },
  { title: 'Seer', img: 'seer.png' },
  { title: 'Sentinel', img: 'sentinel.png' },
  { title: 'Echoist', img: 'echoist.png' },
];

export default function AvatarGallery() {
  return (
    <div>
      {avatars.map((avatar) => (
        <div key={avatar.title}>
          <span>{avatar.title}</span>
          {/* <img src={avatar.img} alt={avatar.title} /> */}
        </div>
      ))}
    </div>
  );
}
