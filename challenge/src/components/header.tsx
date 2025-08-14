"use client"

import * as React from "react"
import Link from "next/link";
import Docs from "@/components/docs";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 w-full bg-gray-900 flex align-center border-b border-gray-700 z-50">
      {/* Logo / Brand Name */}
      {/* <div className="text-2xl font-bold text-white pr-18">My Website logo</div> */}
      <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        
        {/* Navigation Links */}
        <ul className="flex space-x-12 text-gray-300">
          <li><Link href="/" className="hover:text-white cursor-pointer transition-colors">
            <i className="fa-solid fa-sign-in pr-6"></i>Introduction</Link></li>
          <li><Link href="/" className="hover:text-white cursor-pointer transition-colors">
            <i className="fa-solid fa-folder pr-6"></i>Docs</Link></li>
          <li><Link href="/docs" className="hover:text-white cursor-pointer transition-colors">
            <i className="fa-solid fa-download pr-6"></i>Download</Link></li>
          <li><Link href="/" className="hover:text-white cursor-pointer transition-colors">
            <i className="fa-solid fa-list pr-6"></i>Parameters</Link></li>
          <li><Link href="/" className="hover:text-white cursor-pointer transition-colors">
            <i className="fa-solid fa-book pr-6"></i>Output</Link></li>
          <li><Link href="/" className="hover:text-white cursor-pointer transition-colors">
            <i className="fa-solid fa-upload pr-6"></i>Upload</Link></li>
        </ul>
      </nav>
    </header>
  );
}