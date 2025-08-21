import Image from "next/image";
import Header from "@/components/header";
import Footer from "@/components/footer"
import '@fortawesome/fontawesome-free/css/all.min.css';

export default function Docs() {
  const tags = [
    "Plant-based drug discovery",
    "ADMET profiling",
    "Ligand-based pipeline",
    "Bioinformatics",
    "Molecular docking",
    "HPC-compatible bioinformatics"
  ];

  return (
    <div className="bg-gray-900 font-sans min-h-screen flex flex-col">
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

        {/* Docs Content */}
        <div className="max-w-5xl mx-auto px-6 py-12 space-y-10">
          <h1 className="text-3xl text-green-400 font-bold border-b border-green-700 pb-2">Documentation</h1>
          <p className="text-gray-200 text-lg leading-relaxed">
            Welcome to the PhytoDock documentation hub. Here you'll find everything you need to install, configure, 
            and run the pipeline—plus guidance on interpreting results and troubleshooting common issues.
          </p>

          {/* Sections */}
          <section>
            <h2 className="text-2xl text-green-400 font-semibold mb-4">Getting Started</h2>
            <ul className="space-y-4">
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Nextflow Installation</strong>
                <p className="text-gray-300 pl-3"> Step-by-step instructions to install Nextflow on your system (Linux or HPC environments).</p>
              </li>
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Pipeline Installation</strong>
                <p className="text-gray-300 pl-3">How to clone the PhytoDock repository and set up Docker containers for reproducibility.</p>
              </li>
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Pipeline Configuration</strong>
                <p className="text-gray-300 pl-3">Overview of configurable parameters, including input formats, resource settings, and optional flags.</p>
              </li>
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Custom System Config</strong>
                <p className="text-gray-300 pl-3">Instructions for adding your own config profiles to optimize performance on your local or cluster environment.</p>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl text-green-400 font-semibold mb-4">Input Preparation</h2>
            <ul className="space-y-4">
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Reference Compound Setup</strong>
                <p className="text-gray-300 pl-3">How to format and submit your compound using SMILES notation, with examples and validation tips.</p>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl text-green-400 font-semibold mb-4">Running the Pipeline</h2>
            <ul className="space-y-4">
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Execution Guide</strong>
                <p className="text-gray-300 pl-3">A walkthrough of running PhytoDock from start to finish, including command-line examples and expected runtime.</p>
              </li>
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Tutorials & FAQs</strong>
                <p className="text-gray-300 pl-3">Hands-on walkthroughs for first-time users, plus answers to frequently asked questions.</p>
              </li>
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Troubleshooting</strong>
                <p className="text-gray-300 pl-3">Common issues and how to resolve them—covering installation, runtime errors, and output inconsistencies.</p>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl text-green-400 font-semibold mb-4">Output Interpretation</h2>
            <ul className="space-y-4">
              <li className="bg-gray-800 p-4 rounded-xl">
                <strong className="text-green-400">Understanding Results</strong>
                <p className="text-gray-300 pl-3">Explanation of ADMET scores, docking rankings, MD simulation outputs, and how to identify top target candidates.</p>
              </li>
            </ul>
          </section>
        </div>
      </main>

      <Footer/>
    </div>
  );
}
