import Image from "next/image";
import Header from "@/components/header"
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
    
    <div className="bg-gray-800 font-sans min-h-screen flex flex-col">
      <Header/>
      <main className="flex-grow">
        <div className="bg-green-500 text-white flex flex-col justify-center relative z-10 px-24 py-12 mt-12">
          <div className="flex items-center gap-4"> 
            <Image
              aria-hidden
              src="/img/logo.png"
              alt="PhytoDock"
              width="100"
              height={100}
            />
            <h1 className="w-full text-6xl font-bold">PhytoDock</h1>
          </div>
          
          <p className="text-xl font-bold pt-2">A Bioinformatics Pipeline for Traditional Plant-Based Ligands</p>
          <div className="flex flex-wrap gap-2 bg-green-500 pt-2">
            {tags.map((tag) => (
              <span
                key={tag}
                className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
        {/* Introductin section */}
        <div className="px-40 pr-40 py-8 space-y-6">
          <h1 className="text-2xl text-green-500 font-bold">Introduction</h1>
          <p className="text-white text-xl">
            Natural products offer a vast and chemically diverse reservoir of bioactive compounds with promising therapeutic potential. 
            Their unique structural features often contribute to improved safety profiles and efficacy, and they may help overcome drug resistance where synthetic compounds fall short. 
            However, the molecular mechanisms and targets of many natural compounds remain poorly characterized, making mechanism-based optimization and regulatory approval challenging.
          </p>
          <p className="text-white text-xl">
            To address this, identifying disease-relevant protein targets is a critical step in evaluating the therapeutic potential of natural compounds. 
            Yet experimental target identification remains time-consuming, costly, and frequently inconclusive.
          </p>
          <p className="text-white text-xl">
            <strong>PhytoDock</strong> is a scalable, reproducible, and fully automated bioinformatics pipeline designed to bridge this gap. 
            Built using the Nextflow workflow framework, PhytoDock enables high-throughput screening of natural compounds against 17 therapeutic protein classes extracted from the PDBbind database. 
            It is ideal for guiding experimental validation and accelerating early-stage drug discovery from traditional plant-based sources.
          </p>
          <p className="text-white text-xl">
            The pipeline leverages containerized environments (Docker) for easy installation and reproducibility across diverse computing infrastructures, 
            including HPC clusters. Users only need to provide a SMILES representation of the compound and a few customizable parameters—making it accessible even to non-specialists.
          </p>
          <p className="text-white text-xl text-bold">PhytoDock performs:</p>
            <ul className="text-white text-xl list-disc list-inside space-y-1">
              <li><strong>ADMET profiling</strong> to assess pharmacokinetic and safety properties</li>
              <li><strong>Ligand-based molecular docking</strong> to predict binding affinity across curated protein targets</li>
              <li><strong>Short molecular dynamics simulations</strong> to refine docking poses and identify the most probable target candidates</li>
            </ul>
          <p className="text-white text-xl">
            By integrating traditional knowledge with modern computational tools, PhytoDock empowers researchers to uncover the biological potential of natural compounds with speed, precision, and scientific rigor.
          </p>
          <div className="flex justify-center">
            <Image
              aria-hidden
              src="/img/PhytoDock.png"
              alt="PhytoDock"
              width="800"
              height={600}
            />
          </div>
          <p className="text-white text-xl">
            <strong>PhytoDock Pipeline Summary</strong>
          </p>
          <p className="text-white text-xl">
            <strong>PhytoDock</strong> is a fully automated, scalable bioinformatics pipeline designed to identify therapeutic protein targets of natural compounds—especially those derived from traditional medicinal plants. 
            It integrates ligand-based screening, molecular docking, and short molecular dynamics simulations to predict the most probable targets across 17 curated protein classes from the PDBbind database.
          </p>
          <p className="text-white text-xl">Key Features</p>
            <ul className="text-white text-xl list-disc list-inside space-y-1">
              <li><strong>Ligand Input:</strong> Accepts SMILES format for natural compounds</li>
              <li><strong>ADMET Profiling:</strong> Evaluates drug-likeness, toxicity, and pharmacokinetics</li>
              <li><strong>Target Screening:</strong> Docking against 17 therapeutic protein classes</li>
              <li><strong>MD Simulation:</strong> Refines docking poses and ranks target candidates</li>
              <li><strong>Reproducibility:</strong> Built with Nextflow and Docker for seamless deployment across HPC and local systems</li>
              <li><strong>Accessibility:</strong> Minimal input required; suitable for non-specialists</li>
            </ul>
            <p className="text-white text-xl">Workflow Overview</p>
            <div className="flex justify-center "> 
              <Image
                aria-hidden
                src="/img/workflow_light.png"
                alt="PhytoDock"
                width="800"
                height={600}
              />
            </div>
        </div>
      </main>
      <footer className="mt-auto bg-green-600 text-white text-center p-3">
        <p className="text-sm">Authors: Ariungoo, Bayartsetseg Bayarsaikhan, Erdemsaikhan, Maralmaa Gantumur, Munkhjargal, Nomuun, Oyumaa</p>
      </footer>
    </div>
  );
}
