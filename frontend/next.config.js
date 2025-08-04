/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXTAUTH_URL: process.env.NEXTAUTH_URL,
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
    AZURE_AD_CLIENT_ID: process.env.AZURE_AD_CLIENT_ID,
    AZURE_AD_CLIENT_SECRET: process.env.AZURE_AD_CLIENT_SECRET,
    AZURE_AD_TENANT_ID: process.env.AZURE_AD_TENANT_ID,
    API_BASE_URL: process.env.API_BASE_URL,
  },
  async rewrites() {
    return process.env.API_BASE_URL
      ? [
          {
            source: '/api/:path*',
            destination: `${process.env.API_BASE_URL}/api/:path*`,
          },
        ]
      : [];
  },
};

module.exports = nextConfig;