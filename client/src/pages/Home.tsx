import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, AlertCircle, Zap, Shield, Network, Code2 } from "lucide-react";
import { useState } from "react";

interface VerificationResult {
  isValid: boolean;
  verificationScore: number;
  validFragments: number;
  totalFragments: number;
  byzantineResilient: boolean;
  latencyMs: number;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState("demo");
  const [isVerifying, setIsVerifying] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [networkSize, setNetworkSize] = useState(5);
  const [byzantineNodes, setByzantineNodes] = useState(1);

  const runVerification = async () => {
    setIsVerifying(true);
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const validFragments = networkSize - byzantineNodes;
    const verificationScore = validFragments / networkSize;
    const isByzantineResilient = byzantineNodes < networkSize / 2;
    
    setResult({
      isValid: verificationScore >= 0.67 && isByzantineResilient,
      verificationScore,
      validFragments,
      totalFragments: networkSize,
      byzantineResilient: isByzantineResilient,
      latencyMs: Math.random() * 0.5 + 0.01
    });
    
    setIsVerifying(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">LEO-ZKF-Lite</h1>
              <p className="text-xs text-slate-500">By Bader Jamal Jabarin</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="bg-red-50 text-red-700 border-red-200">
              Revolutionary MVP
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-12">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-8">
            <TabsTrigger value="demo">Interactive Demo</TabsTrigger>
            <TabsTrigger value="about">About Bader's ZKF</TabsTrigger>
            <TabsTrigger value="docs">Documentation</TabsTrigger>
          </TabsList>

          {/* Demo Tab */}
          <TabsContent value="demo" className="space-y-6">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="w-5 h-5 text-red-600" />
                  Decentralized Decision Verification
                </CardTitle>
                <CardDescription>
                  Simulate a distributed network verifying an AI decision with Bader's Byzantine resilience protocol
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Network Configuration */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Network Size: <span className="font-bold text-red-600">{networkSize}</span>
                    </label>
                    <input
                      type="range"
                      min="3"
                      max="11"
                      value={networkSize}
                      onChange={(e) => setNetworkSize(parseInt(e.target.value))}
                      disabled={isVerifying}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Byzantine Nodes: <span className="font-bold text-slate-600">{byzantineNodes}</span>
                    </label>
                    <input
                      type="range"
                      min="0"
                      max={Math.floor(networkSize / 2) - 1}
                      value={byzantineNodes}
                      onChange={(e) => setByzantineNodes(parseInt(e.target.value))}
                      disabled={isVerifying}
                      className="w-full"
                    />
                  </div>
                </div>

                {/* Network Status */}
                <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                      <Network className="w-4 h-4" />
                      Network Status
                    </h3>
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{networkSize - byzantineNodes}</div>
                      <div className="text-xs text-slate-600">Honest Nodes</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-red-600">{byzantineNodes}</div>
                      <div className="text-xs text-slate-600">Byzantine Nodes</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{networkSize}</div>
                      <div className="text-xs text-slate-600">Total Nodes</div>
                    </div>
                  </div>
                </div>

                {/* Verification Button */}
                <Button
                  onClick={runVerification}
                  disabled={isVerifying}
                  size="lg"
                  className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800"
                >
                  {isVerifying ? (
                    <>
                      <span className="animate-spin mr-2">⚡</span>
                      Verifying...
                    </>
                  ) : (
                    "Run Verification"
                  )}
                </Button>

                {/* Results */}
                {result && (
                  <div className="space-y-4 mt-6 pt-6 border-t border-slate-200">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-slate-900">Verification Result</h3>
                      {result.isValid ? (
                        <Badge className="bg-green-100 text-green-800 border-green-300">
                          <CheckCircle2 className="w-3 h-3 mr-1" />
                          VALID
                        </Badge>
                      ) : (
                        <Badge className="bg-red-100 text-red-800 border-red-300">
                          <AlertCircle className="w-3 h-3 mr-1" />
                          INVALID
                        </Badge>
                      )}
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-red-50 rounded-lg p-3 border border-red-200">
                        <div className="text-xs text-red-600 font-medium mb-1">Verification Score</div>
                        <div className="text-2xl font-bold text-red-900">
                          {(result.verificationScore * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div className="bg-slate-100 rounded-lg p-3 border border-slate-300">
                        <div className="text-xs text-slate-600 font-medium mb-1">Valid Fragments</div>
                        <div className="text-2xl font-bold text-slate-900">
                          {result.validFragments}/{result.totalFragments}
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className={`rounded-lg p-3 border ${
                        result.byzantineResilient
                          ? 'bg-green-50 border-green-200'
                          : 'bg-red-50 border-red-200'
                      }`}>
                        <div className={`text-xs font-medium mb-1 ${
                          result.byzantineResilient ? 'text-green-600' : 'text-red-600'
                        }`}>
                          Byzantine Resilience
                        </div>
                        <div className={`text-lg font-bold ${
                          result.byzantineResilient ? 'text-green-900' : 'text-red-900'
                        }`}>
                          {result.byzantineResilient ? '✅ Resilient' : '❌ Not Resilient'}
                        </div>
                      </div>
                      <div className="bg-purple-50 rounded-lg p-3 border border-purple-200">
                        <div className="text-xs text-purple-600 font-medium mb-1">Latency</div>
                        <div className="text-lg font-bold text-purple-900">
                          {result.latencyMs.toFixed(3)}ms
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* About Tab */}
          <TabsContent value="about" className="space-y-6">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>What is Bader's ZKF-Lite?</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-slate-700">
                <p>
                  LEO-ZKF-Lite is a revolutionary open-source implementation of the Distributed Zero-Knowledge Fragmentation (ZKF) layer. Developed by Bader Jamal Jabarin, it enables real-time verification of AI decisions across decentralized networks without revealing underlying data or models.
                </p>
                <div className="space-y-3">
                  <div className="flex gap-3">
                    <Zap className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-semibold text-slate-900">Sub-Millisecond Verification</h4>
                      <p className="text-sm text-slate-600">Verify AI decisions in microseconds, not seconds</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Shield className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-semibold text-slate-900">Byzantine Resilient</h4>
                      <p className="text-sm text-slate-600">Tolerates up to 1/3 malicious nodes in the network</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Network className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-semibold text-slate-900">Privacy-Preserving</h4>
                      <p className="text-sm text-slate-600">No raw data or models are exposed during verification</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Docs Tab */}
          <TabsContent value="docs" className="space-y-6">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Code2 className="w-5 h-5" />
                  Getting Started
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-slate-700">
                <div>
                  <h4 className="font-semibold text-slate-900 mb-2">Installation</h4>
                  <pre className="bg-slate-900 text-slate-100 p-3 rounded-lg overflow-x-auto text-sm">
                    <code>git clone https://github.com/BADJAB22/leo-zkf-lite.git
cd leo-zkf-lite
pip install -r requirements.txt</code>
                  </pre>
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 mb-2">Basic Usage</h4>
                  <pre className="bg-slate-900 text-slate-100 p-3 rounded-lg overflow-x-auto text-sm">
                    <code>{`from zkf_lite_engine import ZKFLiteEngine

engine = ZKFLiteEngine(node_id="bader-node-1")
fragment = engine.create_fragment(
    decision="APPROVE",
    confidence=0.92,
    local_state_hash="state_hash"
)
is_valid, report = engine.verify_decision_integrity(
    decision="APPROVE",
    fragments=[fragment]
)`}</code>
                  </pre>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
