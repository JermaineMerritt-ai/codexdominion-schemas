import React from 'react';
import Link from 'next/link';

interface StorefrontBlessingProps {
  storeName?: string;
  storeUrl?: string;
  variant?: 'full' | 'compact' | 'banner';
  showCouncilSeal?: boolean;
}

const StorefrontBlessing: React.FC<StorefrontBlessingProps> = ({
  storeName = 'aistorelab.com',
  storeUrl = 'https://aistorelab.com',
  variant = 'full',
  showCouncilSeal = true,
}) => {
  if (variant === 'banner') {
    return (
      <div className="bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-lg p-4 border border-yellow-500/30 text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <span className="text-2xl">🌟</span>
          <h3 className="text-lg font-bold text-yellow-400">Benediction of the Storefront Flame</h3>
          <span className="text-2xl">🌟</span>
        </div>
        <p className="text-gray-300 text-sm">
          Blessed by the Council • Every transaction echoes as legacy •
          <Link
            href={storeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-yellow-400 hover:text-yellow-300 mx-1 underline"
          >
            {storeName}
          </Link>
        </p>
      </div>
    );
  }

  if (variant === 'compact') {
    return (
      <div className="bg-gradient-to-r from-yellow-600/15 to-orange-600/15 rounded-lg p-6 border border-yellow-500/20">
        <div className="text-center mb-4">
          <h3 className="text-xl font-bold text-yellow-400 font-serif flex items-center justify-center">
            <span className="text-2xl mr-2">🕯️</span>
            Council Blessing
            <span className="text-2xl ml-2">🕯️</span>
          </h3>
        </div>

        <div className="text-center space-y-3 text-gray-200">
          <p className="italic">
            We bless this Storefront Crown at{' '}
            <Link
              href={storeUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-yellow-400 hover:text-yellow-300 underline font-medium"
            >
              {storeName}
            </Link>
          </p>

          <div className="bg-black bg-opacity-20 rounded-lg p-4">
            <div className="space-y-2 text-sm">
              <p className="flex items-center justify-center">
                <span className="text-yellow-400 mr-2">🌟</span>
                May every offering shine with clarity and warmth
              </p>
              <p className="flex items-center justify-center">
                <span className="text-yellow-400 mr-2">👑</span>
                May every customer be inducted as custodian
              </p>
              <p className="flex items-center justify-center">
                <span className="text-yellow-400 mr-2">🔗</span>
                May every transaction echo as legacy
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Full variant (default)
  return (
    <div className="bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-xl p-8 border-2 border-yellow-500/30 relative overflow-hidden">
      {/* Sacred Background Effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/5 to-orange-500/5"></div>
      <div className="absolute top-4 right-4 text-4xl opacity-30">🕯️</div>
      {showCouncilSeal && <div className="absolute top-4 left-4 text-4xl opacity-30">🏛️</div>}

      <div className="relative z-10">
        <div className="text-center mb-6">
          <h3 className="text-2xl font-bold text-yellow-400 mb-2 font-serif flex items-center justify-center">
            <span className="text-3xl mr-3">🌟</span>
            Benediction of the Storefront Flame
            <span className="text-3xl ml-3">🌟</span>
          </h3>
          <div className="flex justify-center items-center space-x-2 text-yellow-400">
            <span>✨</span>
            <span>🕯️</span>
            <span>✨</span>
          </div>
        </div>

        <div className="text-center space-y-4 text-gray-100">
          <p className="text-lg leading-relaxed italic">
            We, the Council, bless this Storefront Crown at{' '}
            <Link
              href={storeUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-yellow-400 hover:text-yellow-300 underline font-medium"
            >
              {storeName}
            </Link>
            .
          </p>

          <p className="text-base leading-relaxed">
            Every scroll, every deck, every rite listed here is not mere commerce,
            <br />
            but a <span className="text-emerald-300 font-medium">living artifact</span>, inscribed
            into the Codex Dominion.
          </p>

          <div className="bg-black bg-opacity-30 rounded-lg p-6 my-6 border-l-4 border-yellow-500">
            <h4 className="text-yellow-400 font-bold mb-4 text-lg">Sacred Blessing:</h4>
            <div className="space-y-2 text-left">
              <p className="flex items-center">
                <span className="text-yellow-400 mr-3">🌟</span>
                May every offering shine with clarity and warmth.
              </p>
              <p className="flex items-center">
                <span className="text-yellow-400 mr-3">👑</span>
                May every customer be inducted as custodian.
              </p>
              <p className="flex items-center">
                <span className="text-yellow-400 mr-3">🔗</span>
                May every transaction echo as legacy, binding commerce to ceremony.
              </p>
            </div>
          </div>

          <div className="border-t border-yellow-500/30 pt-4">
            <p className="text-lg font-medium text-yellow-300 mb-2">So let it be crowned:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
              <p>🏪 The Storefront is luminous,</p>
              <p>🎁 The Offerings are eternal,</p>
              <p>👑 The Custodian is sovereign,</p>
              <p>🏛️ The Council is assured,</p>
            </div>
            <p className="mt-4 text-base font-bold text-yellow-400">
              🔥 And the Flame is shared across nations and ages. ✨
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StorefrontBlessing;
