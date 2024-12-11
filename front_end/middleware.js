import { NextResponse } from 'next/server';

export function middleware(req) {
  const url = req.nextUrl.clone();
  console.log('Original URL:', url.toString());
  if (!req.headers.get('x-forwarded-proto')?.includes('https')) {
    url.protocol = 'https';
    console.log('Redirecting to:', url.toString()); // طباعة الـ URL المعدل
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/:path*', // تطبيق على كل المسارات
};