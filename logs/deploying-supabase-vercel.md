# Deploying a Fullstack App with Supabase and Vercel

> A practical guide to deploying Node.js/React applications with a modern serverless stack.

---

## Overview

In this post, I'll walk through the process of deploying a fullstack application using **Supabase** as the backend and **Vercel** for hosting. This is the stack I used for my Final Degree Project: a management system for an electric cooperative.

## Why This Stack?

- **Supabase**: Open-source Firebase alternative with PostgreSQL, authentication, and real-time subscriptions
- **Vercel**: Zero-config deployments with automatic HTTPS and edge network
- **Cost**: Both offer generous free tiers perfect for small to medium projects

## Step 1: Setting Up Supabase

First, create a new project on [supabase.com](https://supabase.com):

```bash
# Install Supabase CLI
npm install -g supabase

# Login to your account
supabase login

# Initialize in your project
supabase init
```

## Step 2: Database Schema

Define your tables using the Supabase dashboard or migrations:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Step 3: Connect Your React App

Install the Supabase client:

```bash
npm install @supabase/supabase-js
```

Create a client instance:

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
    process.env.REACT_APP_SUPABASE_URL,
    process.env.REACT_APP_SUPABASE_ANON_KEY
)
```

## Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Don't forget to add your environment variables in the Vercel dashboard!

## Lessons Learned

1. **Row Level Security (RLS)** is essential - always enable it
2. Use **environment variables** for all sensitive data
3. Set up **database backups** from day one
4. Monitor your **API usage** to stay within free tier limits

---

*Posted: 2026-01-26*
