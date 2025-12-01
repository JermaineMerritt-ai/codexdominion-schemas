"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = AvatarGallery;
import React from "react";
var avatars = [
    { title: 'Flamekeeper', img: 'flamekeeper.png' },
    { title: 'Archivist', img: 'archivist.png' },
    { title: 'Seer', img: 'seer.png' },
    { title: 'Sentinel', img: 'sentinel.png' },
    { title: 'Echoist', img: 'echoist.png' },
];
function AvatarGallery() {
    return (<div>
      {avatars.map(function (avatar) { return (<div key={avatar.title}>
          <span>{avatar.title}</span>
          {/* <img src={avatar.img} alt={avatar.title} /> */}
        </div>); })}
    </div>);
}
