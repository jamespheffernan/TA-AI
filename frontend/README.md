# TA AI Frontend (Next.js)

## Authentication Setup

This app uses [NextAuth.js](https://next-auth.js.org/) with Azure AD (Microsoft Entra) as the OIDC provider.

### 1. Configure Environment Variables
Copy `.env.example` to `.env.local` and fill in your Azure AD credentials:

```
cp .env.example .env.local
```

Edit `.env.local`:
```
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-random-secret
AZURE_AD_CLIENT_ID=your-azure-client-id
AZURE_AD_CLIENT_SECRET=your-azure-client-secret
AZURE_AD_TENANT_ID=your-tenant-id
API_BASE_URL=http://localhost:7071
```

### 2. Azure AD App Registration
- Register a new app in [Azure Portal](https://portal.azure.com/)
- Set the redirect URI to `http://localhost:3000/api/auth/callback/azure-ad`
- Grant `openid`, `profile`, and `email` permissions
- Copy the client ID, client secret, and tenant ID to your `.env.local`

### 3. Running Locally
```
npm install
npm run dev
```

- Visit [http://localhost:3000](http://localhost:3000)
- You will be prompted to sign in with your Microsoft account

### 4. Protecting Routes
- All `/app` and `/api` routes are protected by default (see `src/middleware.ts`)
- Unauthenticated users are redirected to the sign-in page

---

For more details, see [NextAuth.js Azure AD docs](https://next-auth.js.org/providers/azure-ad).