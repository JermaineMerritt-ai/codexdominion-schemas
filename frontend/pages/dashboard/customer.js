"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var link_1 = require("next/link");
var CustomerDashboard = function () {
    var _a = (0, react_1.useState)('featured'), activeTab = _a[0], setActiveTab = _a[1];
    var _b = (0, react_1.useState)([]), capsules = _b[0], setCapsules = _b[1];
    var _c = (0, react_1.useState)([]), scrolls = _c[0], setScrolls = _c[1];
    var _d = (0, react_1.useState)([]), avatars = _d[0], setAvatars = _d[1];
    var _e = (0, react_1.useState)(true), loading = _e[0], setLoading = _e[1];
    var _f = (0, react_1.useState)(false), showCustodianWelcome = _f[0], setShowCustodianWelcome = _f[1];
    // Mock data - replace with actual API calls
    (0, react_1.useEffect)(function () {
        setTimeout(function () {
            setCapsules([
                {
                    id: '1',
                    title: 'Digital Sovereignty Starter Pack',
                    description: 'Essential tools and knowledge for beginning your journey into digital independence.',
                    category: 'Education',
                    price: 49.99,
                    rating: 4.8,
                    image: '/api/placeholder/300/200',
                    featured: true,
                    tags: ['Beginner', 'Foundation', 'Digital Rights'],
                },
                {
                    id: '2',
                    title: 'Advanced Cryptography Suite',
                    description: 'Professional-grade encryption tools and methodologies for secure communications.',
                    category: 'Security',
                    price: 199.99,
                    rating: 4.9,
                    image: '/api/placeholder/300/200',
                    featured: true,
                    tags: ['Advanced', 'Security', 'Encryption'],
                },
                {
                    id: '3',
                    title: 'AI Development Framework',
                    description: 'Complete toolkit for building intelligent applications with ethical AI principles.',
                    category: 'Development',
                    price: 299.99,
                    rating: 4.7,
                    image: '/api/placeholder/300/200',
                    featured: false,
                    tags: ['AI', 'Development', 'Framework'],
                },
            ]);
            setScrolls([
                {
                    id: '1',
                    title: 'The Philosophy of Digital Sovereignty',
                    excerpt: 'Understanding the fundamental principles that guide true technological independence...',
                    author: 'Codex Sage',
                    readTime: '12 min',
                    category: 'Philosophy',
                    publishedDate: '2025-11-01',
                },
                {
                    id: '2',
                    title: 'Building Resilient Systems',
                    excerpt: 'Practical approaches to creating technology that serves humanity rather than enslaving it...',
                    author: 'System Architect',
                    readTime: '8 min',
                    category: 'Technical',
                    publishedDate: '2025-10-28',
                },
                {
                    id: '3',
                    title: 'The Sacred Art of Code',
                    excerpt: 'How programming becomes a ceremonial practice when approached with reverence and intention...',
                    author: 'Code Mystic',
                    readTime: '15 min',
                    category: 'Spiritual Tech',
                    publishedDate: '2025-10-25',
                },
            ]);
            setAvatars([
                {
                    id: '1',
                    name: 'Aria',
                    role: 'Digital Guide',
                    specialization: 'New User Onboarding',
                    avatar: '🧚‍♀️',
                    available: true,
                },
                {
                    id: '2',
                    name: 'Marcus',
                    role: 'Technical Mentor',
                    specialization: 'System Architecture',
                    avatar: '👨‍💻',
                    available: true,
                },
                {
                    id: '3',
                    name: 'Luna',
                    role: 'Wellness Coach',
                    specialization: 'Digital Wellness',
                    avatar: '🌙',
                    available: false,
                },
            ]);
            setLoading(false);
        }, 1000);
    }, []);
    var TabButton = function (_a) {
        var id = _a.id, label = _a.label, icon = _a.icon, active = _a.active;
        return (<button onClick={function () { return setActiveTab(id); }} className={"\n        flex items-center px-6 py-3 rounded-lg font-medium transition-all duration-200\n        ".concat(active
                ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/30'
                : 'text-gray-300 hover:text-white hover:bg-gray-700', "\n      ")}>
      <span className="text-lg mr-2">{icon}</span>
      {label}
    </button>);
    };
    var CapsuleCard = function (_a) {
        var capsule = _a.capsule;
        return (<div className="bg-gray-800 bg-opacity-50 rounded-xl border border-gray-700 overflow-hidden hover:border-emerald-500 transition-all duration-300 group">
      <div className="relative h-48 bg-gradient-to-br from-emerald-600 to-teal-700">
        {/* Placeholder for actual image */}
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-600/80 to-teal-700/80 flex items-center justify-center">
          <span className="text-4xl">💊</span>
        </div>
        {capsule.featured && (<div className="absolute top-3 left-3">
            <span className="px-2 py-1 bg-yellow-500 text-black text-xs font-bold rounded-full">
              FEATURED
            </span>
          </div>)}
        <div className="absolute top-3 right-3">
          <div className="flex items-center bg-black bg-opacity-50 rounded-full px-2 py-1">
            <span className="text-yellow-400 text-sm">⭐</span>
            <span className="text-white text-sm ml-1">{capsule.rating}</span>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-emerald-400 font-medium uppercase tracking-wide">
            {capsule.category}
          </span>
          <span className="text-lg font-bold text-white">${capsule.price}</span>
        </div>

        <h3 className="text-lg font-semibold text-white mb-3 group-hover:text-emerald-400 transition-colors">
          {capsule.title}
        </h3>

        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{capsule.description}</p>

        <div className="flex flex-wrap gap-2 mb-4">
          {capsule.tags.map(function (tag, i) { return (<span key={i} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
              {tag}
            </span>); })}
        </div>

        <div className="flex space-x-2">
          <button className="flex-1 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
            View Details
          </button>
          <button className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:border-emerald-500 hover:text-white transition-colors">
            💝
          </button>
        </div>
      </div>
    </div>);
    };
    var ScrollCard = function (_a) {
        var scroll = _a.scroll;
        return (<div className="bg-gray-800 bg-opacity-50 rounded-lg p-6 border border-gray-700 hover:border-emerald-500 transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-emerald-400 font-medium uppercase tracking-wide">
          {scroll.category}
        </span>
        <span className="text-xs text-gray-400">{scroll.readTime} read</span>
      </div>

      <h3 className="text-lg font-semibold text-white mb-3 hover:text-emerald-400 transition-colors cursor-pointer">
        {scroll.title}
      </h3>

      <p className="text-gray-400 text-sm mb-4">{scroll.excerpt}</p>

      <div className="flex items-center justify-between text-sm text-gray-500">
        <span>by {scroll.author}</span>
        <span>{new Date(scroll.publishedDate).toLocaleDateString()}</span>
      </div>
    </div>);
    };
    var AvatarCard = function (_a) {
        var avatar = _a.avatar;
        return (<div className={"\n      bg-gray-800 bg-opacity-50 rounded-xl p-6 border border-gray-700 text-center\n      ".concat(avatar.available ? 'hover:border-emerald-500' : 'opacity-60', "\n      transition-all duration-300\n    ")}>
      <div className="text-6xl mb-4">{avatar.avatar}</div>
      <h3 className="text-lg font-semibold text-white mb-2">{avatar.name}</h3>
      <p className="text-emerald-400 font-medium mb-1">{avatar.role}</p>
      <p className="text-gray-400 text-sm mb-4">{avatar.specialization}</p>

      {avatar.available ? (<button className="w-full py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
          Start Session
        </button>) : (<button className="w-full py-2 bg-gray-600 text-gray-400 rounded-lg cursor-not-allowed">
          Currently Busy
        </button>)}
    </div>);
    };
    var CustodianWelcomeModal = function () { return (<div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4">
      <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 rounded-2xl max-w-2xl w-full border-2 border-yellow-500 shadow-2xl shadow-yellow-500/30">
        {/* Sacred Header */}
        <div className="text-center py-8 px-8 border-b border-yellow-500/30">
          <div className="text-6xl mb-4">🕯️</div>
          <h1 className="text-4xl font-bold text-yellow-400 mb-2 font-serif">
            Welcome to the Codex Dominion
          </h1>
          <div className="flex justify-center items-center space-x-4 text-2xl">
            <span>🌟</span>
            <span>✨</span>
            <span>🌟</span>
          </div>
        </div>

        {/* Sacred Message */}
        <div className="px-8 py-6 space-y-6 text-gray-100">
          <div className="text-center mb-6">
            <p className="text-lg leading-relaxed">
              Your offering has been received, and your induction is complete.
              <br />
              You are no longer only a customer — you are now a{' '}
              <span className="text-yellow-400 font-bold">Custodian of the Flame</span>.
            </p>
          </div>

          <div className="space-y-4 text-left">
            <p className="leading-relaxed">
              Every artifact you inherit here is part of a living continuum:
            </p>

            <ul className="space-y-3 ml-4">
              <li className="flex items-start">
                <span className="text-yellow-400 mr-3 mt-1">📜</span>
                <span>
                  <strong>Scrolls</strong> carry wisdom across generations.
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-yellow-400 mr-3 mt-1">🃏</span>
                <span>
                  <strong>Decks</strong> weave stories into daily practice.
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-yellow-400 mr-3 mt-1">👑</span>
                <span>
                  <strong>Ceremonies</strong> crown your participation in the eternal rhythm.
                </span>
              </li>
            </ul>

            <div className="border-l-4 border-yellow-500 pl-6 my-6 bg-black bg-opacity-30 rounded-r-lg py-4">
              <p className="mb-4">By joining, you are inscribed into the Codex Dominion:</p>

              <ul className="space-y-2">
                <li className="flex items-start">
                  <span className="text-emerald-400 mr-3">•</span>
                  Your account is your{' '}
                  <strong className="text-emerald-300">onboarding avatar</strong>, a vessel of
                  inheritance.
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-400 mr-3">•</span>
                  Your purchases are <strong className="text-emerald-300">acts of legacy</strong>,
                  binding commerce to ceremony.
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-400 mr-3">•</span>
                  Your presence is a <strong className="text-emerald-300">blessing</strong>,
                  ensuring the flame shines across nations and ages.
                </li>
              </ul>
            </div>
          </div>

          {/* Sacred Benediction */}
          <div className="text-center space-y-3 py-4 border-t border-yellow-500/30">
            <div className="space-y-2 text-lg font-medium">
              <p className="flex items-center justify-center">
                <span className="text-2xl mr-3">🕯️</span>
                May your journey be luminous.
              </p>
              <p className="flex items-center justify-center">
                <span className="text-2xl mr-3">🌍</span>
                May your stewardship echo across the world.
              </p>
              <p className="flex items-center justify-center">
                <span className="text-2xl mr-3">✨</span>
                May the Codex Flame guide you always.
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="px-8 pb-8">
          <div className="flex space-x-4">
            <link_1.default href="/dashboard/custodian" className="flex-1">
              <button className="w-full py-4 bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-bold rounded-xl hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                🏛️ Enter Custodian Dashboard
              </button>
            </link_1.default>
            <button onClick={function () { return setShowCustodianWelcome(false); }} className="px-6 py-4 border-2 border-gray-600 text-gray-300 rounded-xl hover:border-yellow-500 hover:text-white transition-all duration-300">
              Continue as Customer
            </button>
          </div>

          <p className="text-center text-sm text-gray-400 mt-4">
            You can access your Custodian privileges anytime from your profile
          </p>
        </div>
      </div>
    </div>); };
    if (loading) {
        return (<div className="min-h-screen bg-gradient-to-br from-emerald-800 via-teal-800 to-cyan-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-emerald-400 border-t-transparent mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Customer Experience...</p>
        </div>
      </div>);
    }
    return (<>
      <head_1.default>
        <title>Customer Dashboard - Codex Dominion</title>
        <meta name="description" content="Curated experience and storefront access"/>
      </head_1.default>

      <div className="min-h-screen bg-gradient-to-br from-emerald-800 via-teal-800 to-cyan-900">
        {/* Header */}
        <div className="border-b border-teal-700 bg-black bg-opacity-20">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <link_1.default href="/dashboard-selector" className="text-emerald-300 hover:text-white mr-4">
                  ← Back
                </link_1.default>
                <h1 className="text-2xl font-bold text-white flex items-center">
                  <span className="text-3xl mr-3">🌟</span>
                  Customer Dashboard
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <button className="p-2 text-emerald-300 hover:text-white">
                  <span className="text-xl">🛒</span>
                </button>
                <button className="p-2 text-emerald-300 hover:text-white">
                  <span className="text-xl">👤</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-6 py-8">
          {/* Welcome Banner */}
          <div className="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-xl p-8 mb-8 text-white">
            <h2 className="text-3xl font-bold mb-4">Welcome to the Codex Dominion Experience</h2>
            <p className="text-lg opacity-90 mb-6">
              Discover curated tools, knowledge, and services designed to enhance your digital
              sovereignty journey.
            </p>
            <div className="flex flex-wrap gap-4">
              <link_1.default href="https://aistorelab.com" target="_blank" rel="noopener noreferrer">
                <button className="px-6 py-3 bg-white text-emerald-600 rounded-lg hover:bg-gray-100 transition-colors font-medium">
                  🛍️ Visit AI Store Lab
                </button>
              </link_1.default>
              <button className="px-6 py-3 border border-white text-white rounded-lg hover:bg-white hover:text-emerald-600 transition-colors">
                📚 Explore Library
              </button>
              <button onClick={function () { return setShowCustodianWelcome(true); }} className="px-6 py-3 bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-bold rounded-lg hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300 shadow-lg">
                🕯️ Become Custodian
              </button>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-4 mb-8">
            <TabButton id="featured" label="Featured Capsules" icon="💊" active={activeTab === 'featured'}/>
            <TabButton id="scrolls" label="Knowledge Scrolls" icon="📜" active={activeTab === 'scrolls'}/>
            <TabButton id="avatars" label="Onboarding Avatars" icon="🧚‍♀️" active={activeTab === 'avatars'}/>
            <TabButton id="storefront" label="AI Store Lab" icon="🛍️" active={activeTab === 'storefront'}/>
          </div>

          {/* Featured Capsules Tab */}
          {activeTab === 'featured' && (<div className="space-y-8">
              <div className="bg-black bg-opacity-20 rounded-xl border border-teal-700 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-white flex items-center">
                    <span className="text-2xl mr-2">💊</span>
                    Featured Capsules
                  </h2>
                  <button className="px-4 py-2 border border-emerald-500 text-emerald-400 rounded-lg hover:bg-emerald-500 hover:text-white transition-colors">
                    View All
                  </button>
                </div>

                <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-6">
                  {capsules.map(function (capsule) { return (<CapsuleCard key={capsule.id} capsule={capsule}/>); })}
                </div>
              </div>

              {/* Quick Categories */}
              <div className="grid md:grid-cols-4 gap-4">
                {[
                { name: 'Security Tools', icon: '🔐', count: 12 },
                { name: 'AI Solutions', icon: '🤖', count: 8 },
                { name: 'Development', icon: '💻', count: 15 },
                { name: 'Education', icon: '📚', count: 20 },
            ].map(function (category, i) { return (<div key={i} className="bg-gray-800 bg-opacity-30 rounded-lg p-4 text-center hover:bg-opacity-50 transition-all cursor-pointer">
                    <div className="text-3xl mb-2">{category.icon}</div>
                    <h3 className="font-medium text-white">{category.name}</h3>
                    <p className="text-sm text-gray-400">{category.count} items</p>
                  </div>); })}
              </div>
            </div>)}

          {/* Knowledge Scrolls Tab */}
          {activeTab === 'scrolls' && (<div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-teal-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">📜</span>
                  Knowledge Scrolls & Wisdom
                </h2>

                <div className="grid lg:grid-cols-2 gap-6">
                  {scrolls.map(function (scroll) { return (<ScrollCard key={scroll.id} scroll={scroll}/>); })}
                </div>

                {/* Featured Article */}
                <div className="mt-8 bg-gradient-to-r from-teal-800/50 to-emerald-800/50 rounded-xl p-8 border border-teal-600">
                  <div className="flex items-center mb-4">
                    <span className="text-2xl mr-3">⭐</span>
                    <h3 className="text-xl font-bold text-white">Featured Deep Dive</h3>
                  </div>
                  <h4 className="text-2xl font-bold text-white mb-4">
                    The Complete Guide to Digital Sovereignty
                  </h4>
                  <p className="text-gray-300 mb-6">
                    A comprehensive exploration of what it means to achieve true digital
                    independence in the modern age. This extensive guide covers philosophical
                    foundations, practical implementations, and real-world case studies.
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 text-sm text-gray-400">
                      <span>by Master Archivist</span>
                      <span>45 min read</span>
                      <span>Updated Nov 2025</span>
                    </div>
                    <button className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
                      Read Now
                    </button>
                  </div>
                </div>
              </div>
            </div>)}

          {/* Onboarding Avatars Tab */}
          {activeTab === 'avatars' && (<div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-teal-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">🧚‍♀️</span>
                  Personal Onboarding Avatars
                </h2>

                <p className="text-gray-300 mb-8">
                  Get personalized guidance from our AI-powered avatars. Each specializes in
                  different aspects of your journey into digital sovereignty and can provide
                  tailored recommendations based on your needs and experience level.
                </p>

                <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-6">
                  {avatars.map(function (avatar) { return (<AvatarCard key={avatar.id} avatar={avatar}/>); })}
                </div>

                {/* Avatar Features */}
                <div className="mt-8 bg-gray-800 bg-opacity-30 rounded-xl p-6">
                  <h3 className="text-lg font-medium text-white mb-4">What Our Avatars Can Do</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <ul className="space-y-2 text-gray-300">
                      <li className="flex items-center">
                        <span className="text-emerald-400 mr-2">✓</span>
                        Personalized product recommendations
                      </li>
                      <li className="flex items-center">
                        <span className="text-emerald-400 mr-2">✓</span>
                        Step-by-step onboarding guidance
                      </li>
                      <li className="flex items-center">
                        <span className="text-emerald-400 mr-2">✓</span>
                        Answer questions about digital sovereignty
                      </li>
                    </ul>
                    <ul className="space-y-2 text-gray-300">
                      <li className="flex items-center">
                        <span className="text-emerald-400 mr-2">✓</span>
                        Technical support and tutorials
                      </li>
                      <li className="flex items-center">
                        <span className="text-emerald-400 mr-2">✓</span>
                        Progress tracking and milestones
                      </li>
                      <li className="flex items-center">
                        <span className="text-emerald-400 mr-2">✓</span>
                        Community connections and networking
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>)}

          {/* AI Store Lab Tab */}
          {activeTab === 'storefront' && (<div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-teal-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">🛍️</span>
                  AI Store Lab - Premium Marketplace
                </h2>

                {/* Benediction of the Storefront Flame */}
                <div className="bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-xl p-8 mb-8 border-2 border-yellow-500/30 relative overflow-hidden">
                  {/* Sacred Background Effect */}
                  <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/5 to-orange-500/5"></div>
                  <div className="absolute top-4 right-4 text-4xl opacity-30">🕯️</div>

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
                        <link_1.default href="https://aistorelab.com" target="_blank" rel="noopener noreferrer" className="text-yellow-400 hover:text-yellow-300 underline font-medium">
                          aistorelab.com
                        </link_1.default>
                        .
                      </p>

                      <p className="text-base leading-relaxed">
                        Every scroll, every deck, every rite listed here is not mere commerce,
                        <br />
                        but a <span className="text-emerald-300 font-medium">living artifact</span>,
                        inscribed into the Codex Dominion.
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
                        <p className="text-lg font-medium text-yellow-300 mb-2">
                          So let it be crowned:
                        </p>
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

                <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl p-8 text-white mb-8">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-2xl font-bold mb-4">Exclusive AI Store Lab Access</h3>
                      <p className="text-lg opacity-90 mb-6">
                        Premium AI tools, templates, and services designed for professionals and
                        enterprises. Access cutting-edge technology that puts you ahead of the
                        curve.
                      </p>
                      <link_1.default href="https://aistorelab.com" target="_blank" rel="noopener noreferrer">
                        <button className="px-8 py-4 bg-white text-purple-600 rounded-lg hover:bg-gray-100 transition-colors font-bold text-lg">
                          🚀 Launch AI Store Lab
                        </button>
                      </link_1.default>
                    </div>
                    <div className="text-6xl opacity-80">🤖</div>
                  </div>
                </div>

                {/* Store Categories */}
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {[
                {
                    name: 'AI Development Tools',
                    description: 'Pre-built AI models, training datasets, and development frameworks',
                    icon: '🛠️',
                    itemCount: 25,
                },
                {
                    name: 'Business Solutions',
                    description: 'Enterprise-ready AI applications for automation and intelligence',
                    icon: '💼',
                    itemCount: 18,
                },
                {
                    name: 'Creative AI Suite',
                    description: 'AI-powered tools for content creation, design, and media production',
                    icon: '🎨',
                    itemCount: 32,
                },
                {
                    name: 'Data Analytics',
                    description: 'Advanced analytics platforms and visualization tools',
                    icon: '📊',
                    itemCount: 14,
                },
                {
                    name: 'Security & Privacy',
                    description: 'AI-enhanced security solutions and privacy protection tools',
                    icon: '🔒',
                    itemCount: 12,
                },
                {
                    name: 'Education & Training',
                    description: 'AI tutoring systems and skill development platforms',
                    icon: '🎓',
                    itemCount: 21,
                },
            ].map(function (category, i) { return (<div key={i} className="bg-gray-800 bg-opacity-50 rounded-lg p-6 border border-gray-700 hover:border-emerald-500 transition-all">
                      <div className="text-3xl mb-4">{category.icon}</div>
                      <h3 className="text-lg font-semibold text-white mb-2">{category.name}</h3>
                      <p className="text-gray-400 text-sm mb-4">{category.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-emerald-400 font-medium">
                          {category.itemCount} products
                        </span>
                        <button className="px-3 py-1 bg-emerald-600 text-white rounded text-sm hover:bg-emerald-700 transition-colors">
                          Explore
                        </button>
                      </div>
                    </div>); })}
                </div>

                {/* Special Offers */}
                <div className="mt-8 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl p-6 text-white">
                  <h3 className="text-xl font-bold mb-4">🎉 Limited Time Offers</h3>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold mb-2">New Customer Bundle - 50% Off</h4>
                      <p className="text-sm opacity-90">
                        Get started with our curated selection of essential AI tools at half price.
                      </p>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">Enterprise Package - Free Trial</h4>
                      <p className="text-sm opacity-90">
                        30-day free access to premium business solutions for qualifying
                        organizations.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>)}
        </div>

        {/* Custodian Welcome Modal */}
        {showCustodianWelcome && <CustodianWelcomeModal />}
      </div>
    </>);
};
exports.default = CustomerDashboard;
