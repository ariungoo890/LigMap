"use client"

import * as React from "react"

export default function Footer() {
  return (
    <footer className="mt-auto bg-gray-800 border-t border-green-700 text-gray-300 text-center py-6">
        <p className="text-sm">🌱 Authors: Ariungoo, Bayartsetseg, Erdemsaikhan, Maralmaa, Munkhjargal, Nomuun, Oyumaa</p>
        <p className="text-xs text-gray-500">© {new Date().getFullYear()} PhytoDock Project</p>
    </footer>
  );
}
