"use client";

import { useState } from "react";

export default function CreateShopifyStorePage() {
  const [formData, setFormData] = useState({
    brand_name: "",
    brand_description: "",
    primary_color: "#F5C542",
    secondary_color: "#10B981",
    primary_font: "Inter",
    secondary_font: "Roboto",
    target_countries: [],
    default_currency: "USD",
    shop_owner_email: "",
    product_categories: [],
    initial_products_count: 5,
    shopify_store_type: "new",
    existing_shopify_domain: ""
  });

  const [categoryInput, setCategoryInput] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [workflowId, setWorkflowId] = useState(null);

  const fonts = ["Inter", "Roboto", "Lora", "Playfair Display", "Open Sans", "Montserrat"];
  const currencies = ["USD", "CAD", "EUR", "GBP", "AUD"];
  const countries = ["US", "CA", "UK", "AU", "DE", "FR", "ES", "IT"];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCountryToggle = (country) => {
    const current = formData.target_countries;
    if (current.includes(country)) {
      setFormData({ ...formData, target_countries: current.filter(c => c !== country) });
    } else {
      setFormData({ ...formData, target_countries: [...current, country] });
    }
  };

  const handleAddCategory = () => {
    if (categoryInput.trim()) {
      setFormData({
        ...formData,
        product_categories: [...formData.product_categories, categoryInput.trim()]
      });
      setCategoryInput("");
    }
  };

  const handleRemoveCategory = (index) => {
    setFormData({
      ...formData,
      product_categories: formData.product_categories.filter((_, i) => i !== index)
    });
  };

  const calculateSavings = () => {
    const tasks_per_week = 30;
    const time_per_task = 25;
    const hourly_wage = 45;
    const automation_percent = 0.8;
    
    const hours_saved = (tasks_per_week * (time_per_task / 60) * automation_percent).toFixed(1);
    const weekly_savings = (hours_saved * hourly_wage).toFixed(0);
    
    return { hours_saved, weekly_savings };
  };

  const savings = calculateSavings();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await fetch("/api/workflows/start/store.create_shopify_store", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setWorkflowId(data.workflow_id);
      } else {
        alert("Failed to create workflow");
      }
    } catch (error) {
      alert("Error: " + error.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (workflowId) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
        <div className="max-w-2xl mx-auto">
          <div className="border border-emerald-500 bg-emerald-950/20 rounded-lg p-8 text-center">
            <div className="text-4xl mb-4">✅</div>
            <h1 className="text-2xl font-bold mb-2">Workflow Created</h1>
            <p className="text-slate-400 mb-4">
              Your Shopify store creation workflow has been submitted to the Commerce Council for review.
            </p>
            <div className="font-mono text-emerald-400 mb-6">
              Workflow ID: {workflowId}
            </div>
            <div className="flex gap-4 justify-center">
              <a
                href={`/dashboard/workflows/${workflowId}`}
                className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 rounded"
              >
                View Workflow
              </a>
              <a
                href="/dashboard/workflows"
                className="px-6 py-2 bg-slate-800 hover:bg-slate-700 rounded"
              >
                Back to Catalog
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Create Shopify Store</h1>
          <p className="text-slate-400">
            Define your brand and CodexDominion will generate and configure your store.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* A. Brand Identity */}
          <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 text-emerald-400">Brand Identity</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Brand Name *</label>
                <input
                  type="text"
                  name="brand_name"
                  value={formData.brand_name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Brand Description *</label>
                <textarea
                  name="brand_description"
                  value={formData.brand_description}
                  onChange={handleChange}
                  required
                  rows={4}
                  placeholder="What is this brand? What does it sell? Who is it for?"
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Primary Color</label>
                  <input
                    type="color"
                    name="primary_color"
                    value={formData.primary_color}
                    onChange={handleChange}
                    className="w-full h-12 bg-slate-950 border border-slate-700 rounded cursor-pointer"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Secondary Color</label>
                  <input
                    type="color"
                    name="secondary_color"
                    value={formData.secondary_color}
                    onChange={handleChange}
                    className="w-full h-12 bg-slate-950 border border-slate-700 rounded cursor-pointer"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Primary Font</label>
                  <select
                    name="primary_font"
                    value={formData.primary_font}
                    onChange={handleChange}
                    className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                  >
                    {fonts.map(font => (
                      <option key={font} value={font}>{font}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Secondary Font</label>
                  <select
                    name="secondary_font"
                    value={formData.secondary_font}
                    onChange={handleChange}
                    className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                  >
                    {fonts.map(font => (
                      <option key={font} value={font}>{font}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* B. Market & Currency */}
          <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 text-emerald-400">Market & Currency</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Target Countries *</label>
                <div className="flex flex-wrap gap-2">
                  {countries.map(country => (
                    <button
                      key={country}
                      type="button"
                      onClick={() => handleCountryToggle(country)}
                      className={`px-4 py-2 rounded border ${
                        formData.target_countries.includes(country)
                          ? "bg-emerald-600 border-emerald-500"
                          : "bg-slate-950 border-slate-700"
                      }`}
                    >
                      {country}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Default Currency *</label>
                <select
                  name="default_currency"
                  value={formData.default_currency}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                >
                  {currencies.map(currency => (
                    <option key={currency} value={currency}>{currency}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Shop Owner Email *</label>
                <input
                  type="email"
                  name="shop_owner_email"
                  value={formData.shop_owner_email}
                  onChange={handleChange}
                  required
                  placeholder="owner@example.com"
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                />
              </div>
            </div>
          </div>

          {/* C. Products */}
          <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 text-emerald-400">Products</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Product Categories</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={categoryInput}
                    onChange={(e) => setCategoryInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), handleAddCategory())}
                    placeholder="e.g. skin care, digital courses"
                    className="flex-1 px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                  />
                  <button
                    type="button"
                    onClick={handleAddCategory}
                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 rounded"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.product_categories.map((cat, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-slate-950 border border-slate-700 rounded flex items-center gap-2"
                    >
                      {cat}
                      <button
                        type="button"
                        onClick={() => handleRemoveCategory(index)}
                        className="text-slate-400 hover:text-slate-200"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Initial Products Count</label>
                <input
                  type="number"
                  name="initial_products_count"
                  value={formData.initial_products_count}
                  onChange={handleChange}
                  min={1}
                  max={50}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                />
              </div>
            </div>
          </div>

          {/* D. Shopify Connection */}
          <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 text-emerald-400">Shopify Connection</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Store Type *</label>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="shopify_store_type"
                      value="new"
                      checked={formData.shopify_store_type === "new"}
                      onChange={handleChange}
                      className="text-emerald-500"
                    />
                    <span>Create new Shopify store</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="shopify_store_type"
                      value="existing"
                      checked={formData.shopify_store_type === "existing"}
                      onChange={handleChange}
                      className="text-emerald-500"
                    />
                    <span>Connect existing Shopify store</span>
                  </label>
                </div>
              </div>

              {formData.shopify_store_type === "existing" && (
                <div>
                  <label className="block text-sm font-medium mb-2">Existing Shopify Domain *</label>
                  <input
                    type="text"
                    name="existing_shopify_domain"
                    value={formData.existing_shopify_domain}
                    onChange={handleChange}
                    placeholder="your-store.myshopify.com"
                    required={formData.shopify_store_type === "existing"}
                    className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              )}
            </div>
          </div>

          {/* E. Governance & Impact Preview */}
          <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 text-emerald-400">Governance & Impact Preview</h2>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-slate-400">Council</div>
                  <div className="font-medium">Commerce Council</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Requires Review</div>
                  <div className="font-medium">Yes</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Auto Execute</div>
                  <div className="font-medium">No</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Risk Flags</div>
                  <div className="flex flex-wrap gap-1">
                    <span className="px-2 py-1 bg-yellow-600/20 border border-yellow-600 rounded text-xs">
                      Public-facing
                    </span>
                    <span className="px-2 py-1 bg-yellow-600/20 border border-yellow-600 rounded text-xs">
                      Financial
                    </span>
                    <span className="px-2 py-1 bg-yellow-600/20 border border-yellow-600 rounded text-xs">
                      Brand-sensitive
                    </span>
                  </div>
                </div>
              </div>

              <div className="border-t border-slate-700 pt-4 mt-4">
                <div className="text-sm text-slate-400 mb-2">Estimated Savings</div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-2xl font-bold text-emerald-400">{savings.hours_saved}h</div>
                    <div className="text-sm text-slate-400">Hours saved per week</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-emerald-400">${savings.weekly_savings}</div>
                    <div className="text-sm text-slate-400">Weekly dollar savings</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* F. Submit */}
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-4 bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-700 disabled:cursor-not-allowed rounded font-bold text-lg"
          >
            {submitting ? "Creating Workflow..." : "Create Shopify Store Workflow →"}
          </button>
        </form>
      </div>
    </div>
  );
}
