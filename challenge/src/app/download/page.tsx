"use client"

import * as React from "react"
import { useState } from "react";
import Header from "@/components/header"
import Footer from "@/components/footer"
import Image from "next/image";
import Link from "next/link";

export default function Parameters() {

  const [singleStranded, setSingleStranded] = useState(false);
  const [singleEnd, setSingleEnd] = useState(false);
  const [bam, setBam] = useState(false);
  const [udgType, setUdgType] = useState("none");
  const [colourChemistry, setColourChemistry] = useState("4");
  const tags = [
    "Plant-based drug discovery",
    "ADMET profiling",
    "Ligand-based pipeline",
    "Bioinformatics",
    "Molecular docking",
    "HPC-compatible bioinformatics"
  ];

  return (
    <div className="bg-gray-800 font-sans min-h-screen flex flex-col">
        <Header/>
        <main className="flex-grow">
          {/* Hero Section */}
          <div className="relative bg-gradient-to-r from-green-700 to-green-400 text-white pl-100 py-16 mt-12 rounded-b-3xl shadow-lg">
            <div className="flex items-center gap-6">
              <Image
                aria-hidden
                src="/img/logo.png"
                alt="PhytoDock"
                width="100"
                height={100}
                className="rounded-lg"
              />
              <h1 className="text-6xl font-extrabold tracking-tight">PhytoDock</h1>
            </div>
                    
            <p className="text-2xl font-semibold pt-4">
              A Bioinformatics Pipeline for Traditional Plant-Based Ligands
            </p>
                    
            <div className="flex flex-wrap gap-2 pt-4">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="bg-green-700/80 hover:bg-green-800 transition-colors text-white px-4 py-1.5 rounded-full text-sm font-medium shadow"
                  >
                  {tag}
                </span>
                ))}
            </div>
          </div>

            <div className="bg-gray-900 text-gray-200 p-6 my-6 rounded-xl shadow-lg max-w-3xl mx-auto space-y-6">
              <h2 className="text-xl font-bold text-green-400">Download Link</h2>
              <Link href="https://github.com/ariungoo890/LigMap" className="underline"><i className="fa-brands fa-github pr-6"></i>https://github.com/ariungoo890/LigMap</Link>
            </div>
        </main>
        <Footer/>
    </div>

  );
}
