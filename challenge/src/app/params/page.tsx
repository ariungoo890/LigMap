"use client"

import * as React from "react"
import { useState } from "react";
import Header from "@/components/header"
import Footer from "@/components/footer"
import Image from "next/image";

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

              <h2 className="text-xl font-bold text-green-400">💻 Input/output options</h2>
              <p className="text-sm text-gray-400">
                Define where the pipeline should find input data, and additional metadata.
              </p>

              <div>
                <label className="block text-sm font-medium mb-1">SMILES:</label>
                <input
                  type="text"
                  placeholder="Example: OC1=CC=C(\C=C\C2=C3C(C(OC3=CC3=C2C(C(O3)C2=CC=C(O)C=C2)C2=CC(O)=CC(O)=C2)C2=CC=C(O)C=C2)C2=CC(O)=CC(O)=C2)C=C1"
                  className="w-full p-2 rounded bg-gray-800 border border-gray-700 focus:border-green-400 focus:outline-none"
                />
                <p className="text-xs text-gray-500 mt-1">
                   Stands for <strong>Simplified Molecular-Input Line-Entry System.</strong> This parameter provides a linear notation of the ligand molecule's structure. 
                   It's a way to represent the molecule's atoms and bonds in a simple text string, which can be useful for identification and structural verification.
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Ligand_charge:</label>
                <input
                  type="text"
                  placeholder="0"
                  className="w-full p-2 rounded bg-gray-800 border border-gray-700 focus:border-green-400 focus:outline-none"
                />
                <p className="text-xs text-gray-500 mt-1">
                   This is the <strong>total net charge</strong> of the ligand molecule. 
                   It's an integer value representing the sum of formal charges on all atoms in the ligand. 
                   For many organic molecules, this value is 0.
                </p>
              </div>

              {/* --single_stranded */}
              <div>
                <label className="block text-sm font-medium mb-1">Ligand_input_path:</label>
                <input
                  type="text"
                  placeholder="/home/bayar/Documents/input/ligand_trial.pdb"
                  className="w-full p-2 rounded bg-gray-800 border border-gray-700 focus:border-green-400 focus:outline-none"
                />
                <p className="text-xs text-gray-500 mt-1">
                   This parameter specifies the <strong>file path</strong> to the ligand's three-dimensional structure. 
                   The script uses this path to locate the PDB (Protein Data Bank) file, which contains the atomic coordinates of the ligand.
                </p>
              </div>

              {/* --colour_chemistry */}
              <div>
                <label className="block text-sm font-medium mb-1">Target_selection:</label>
                <select
                  value={colourChemistry}
                  onChange={(e) => setColourChemistry(e.target.value)}
                  className="w-full p-2 rounded bg-gray-800 border border-gray-700"
                >
                  <option value="2">1tou</option>
                  <option value="4">2qcm</option>
                  <option value="2">2sim</option>
                  <option value="4">2v4c</option>
                  <option value="4">3t1l</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                   This parameter lists the <strong>PDB IDs of the protein targets</strong> selected for docking. 
                   The script uses this list to identify which protein structures to download and prepare for the docking simulation. 
                   The targets are separated by spaces or commas.
                </p>
              </div>
            </div>
        </main>
        <Footer/>
    </div>

  );
}
