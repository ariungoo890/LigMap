"use client"

import * as React from "react"
import Image from "next/image";
import Link from "next/link";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 w-full bg-gray-900/80 backdrop-blur-md shadow-md border-b border-gray-700 z-50">
      <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center text-xl font-bold text-white tracking-wide">
          <Image
            aria-hidden
            src="/img/logo.png"
            alt="PhytoDock"
            width="24"
            height={100}
            className="rounded-lg mr-2"
          />
           PhytoDock
        </div>

        {/* Navigation Links */}
        <ul className="hidden md:flex space-x-10 text-gray-300 font-medium">
          <li>
            <Link href="/" className="group flex items-center hover:text-white transition">
              <i className="fa-solid fa-sign-in mr-2"></i>
              Introduction
              <span className="block h-0.5 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
            </Link>
          </li>
          <li>
            <Link href="/docs" className="group flex items-center hover:text-white transition">
              <i className="fa-solid fa-folder mr-2"></i>
              Docs
              <span className="block h-0.5 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
            </Link>
          </li>
          <li>
            <Link href="/download" className="group flex items-center hover:text-white transition">
              <i className="fa-solid fa-download mr-2"></i>
              Download
              <span className="block h-0.5 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
            </Link>
          </li>
          <li>
            <Link href="/params" className="group flex items-center hover:text-white transition">
              <i className="fa-solid fa-list mr-2"></i>
              Parameters
              <span className="block h-0.5 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
            </Link>
          </li>
          <li>
            <Link href="/params" className="group flex items-center hover:text-white transition">
              <i className="fa-solid fa-book mr-2"></i>
              Output
              <span className="block h-0.5 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
            </Link>
          </li>
          <li>
            <Link href="/" className="group flex items-center hover:text-white transition">
              <i className="fa-solid fa-upload mr-2"></i>
              Upload
              <span className="block h-0.5 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
            </Link>
          </li>
        </ul>

        {/* Mobile Menu (hamburger) */}
        <button className="md:hidden text-white text-2xl focus:outline-none">
          <i className="fa-solid fa-bars"></i>
        </button>
      </nav>
    </header>
  );
}
