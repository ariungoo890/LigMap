import Image from "next/image";
import Header from "@/components/header"
import Footer from "@/components/footer"
import '@fortawesome/fontawesome-free/css/all.min.css';

export default function Home() {
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

        {/* Introduction Section */}
        <div className="max-w-5xl mx-auto px-6 py-12 space-y-10">
          <h2 className="text-3xl text-green-400 font-bold border-b border-green-700 pb-2">Introduction</h2>

          <div className="space-y-6 text-lg leading-relaxed text-gray-200">
            <p>
              Natural products offer a vast and chemically diverse reservoir of bioactive compounds with promising therapeutic potential. 
              Their unique structural features often contribute to improved safety profiles and efficacy, and they may help overcome drug resistance where synthetic compounds fall short. 
              However, the molecular mechanisms and targets of many natural compounds remain poorly characterized, making mechanism-based optimization and regulatory approval challenging.
            </p>
            <p>
              To address this, identifying disease-relevant protein targets is a critical step in evaluating the therapeutic potential of natural compounds. 
              Yet experimental target identification remains time-consuming, costly, and frequently inconclusive.
            </p>
            <p>
              <strong className="text-green-400">PhytoDock</strong> is a scalable, reproducible, and fully automated bioinformatics pipeline designed to bridge this gap. 
              Built using the Nextflow workflow framework, PhytoDock enables high-throughput screening of natural compounds against 17 therapeutic protein classes extracted from the PDBbind database. 
              It is ideal for guiding experimental validation and accelerating early-stage drug discovery from traditional plant-based sources.
            </p>
            <p>
              The pipeline leverages containerized environments (Docker) for easy installation and reproducibility across diverse computing infrastructures, including HPC clusters. 
              Users only need to provide a SMILES representation of the compound and a few customizable parameters—making it accessible even to non-specialists.
            </p>
          </div>

          <div>
            <h3 className="text-2xl text-green-400 font-semibold mb-3">PhytoDock performs:</h3>
            <ul className="space-y-3 text-gray-200 text-lg">
              <li><i className="fas fa-check-circle text-green-400 mr-2"></i><strong>ADMET profiling</strong> to assess pharmacokinetic and safety properties</li>
              <li><i className="fas fa-check-circle text-green-400 mr-2"></i><strong>Ligand-based molecular docking</strong> to predict binding affinity across curated protein targets</li>
              <li><i className="fas fa-check-circle text-green-400 mr-2"></i><strong>Short molecular dynamics simulations</strong> to refine docking poses and identify the most probable target candidates</li>
            </ul>
          </div>

          <div className="space-y-6 text-lg leading-relaxed text-gray-200">
            <p>
              By integrating traditional knowledge with modern computational tools, PhytoDock empowers researchers to uncover the biological potential of natural compounds with speed, precision, and scientific rigor.
            </p>
          </div>

          <div className="space-y-6 text-lg leading-relaxed text-gray-200">
            <h3 className="text-2xl text-green-400 font-semibold mb-3">PhytoDock Pipeline Summary</h3>
            <p>
              <strong>PhytoDock</strong> is a fully automated, scalable bioinformatics pipeline designed to identify therapeutic protein targets of natural compounds—especially those derived from traditional medicinal plants. 
              It integrates ligand-based screening, molecular docking, and short molecular dynamics simulations to predict the most probable targets across 17 curated protein classes from the PDBbind database.
            </p>
          </div>

          <div className="flex justify-center py-6">
            <Image
              aria-hidden
              src="/img/PhytoDock.png"
              alt="PhytoDock Pipeline"
              width="800"
              height="600"
              className="rounded-xl shadow-lg border border-gray-700"
            />
          </div>

          <div className="space-y-6 text-lg leading-relaxed text-gray-200">
            <h2 className="text-xl text-green-400 font-semibold">Key Features</h2>
            <ul className="space-y-2 text-gray-200 text-lg">
              <li><i className="fas fa-leaf text-green-400 mr-2"></i><strong>Ligand Input:</strong>  Accepts SMILES format for natural compounds</li>
              <li><i className="fas fa-vial text-green-400 mr-2"></i><strong>ADMET Profiling:</strong> Evaluates drug-likeness, toxicity, and pharmacokinetics</li>
              <li><i className="fas fa-dna text-green-400 mr-2"></i><strong>Target Screening:</strong> Docking against 17 therapeutic protein classes</li>
              <li><i className="fas fa-project-diagram text-green-400 mr-2"></i><strong>MD Simulation:</strong> Refines docking poses and ranks target candidates</li>
              <li><i className="fas fa-cubes text-green-400 mr-2"></i><strong>Reproducibility:</strong> Built with Nextflow and Docker for seamless deployment across HPC and local systems</li>
              <li><i className="fas fa-user-friends text-green-400 mr-2"></i><strong>Accessibility:</strong> Minimal input required; suitable for non-specialists</li>
            </ul>
          </div>

          <div className="flex justify-center py-6">
            <Image
              aria-hidden
              src="/img/workflow_light.png"
              alt="Workflow"
              width="800"
              height="600"
              className="rounded-xl shadow-lg border border-gray-700"
            />
          </div>
        </div>
      </main>

      <Footer/>
    </div>
  );
}
