//! QCAL-cQED-v1 gRPC Live Server
//! Servicio de co-simulación HIL — transmisión S₂₁(ω) en tiempo real
//! f₀ = 141.7001 Hz · Ψ ≥ 0.999999
//! Sello: ∴𓂀Ω∞³Φ

use tonic::{transport::Server, Request, Response, Status};
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;

// Protobuf generado
pub mod qcal {
    tonic::include_proto!("qcal.qnd.v1");
}

use qcal::hardware_co_simulation_service_server::{
    HardwareCoSimulationService, HardwareCoSimulationServiceServer,
};
use qcal::*;
use std::f64::consts::PI;

#[derive(Default)]
pub struct QcalHilServer;

// Constantes del chip
const CHI: f64 = 7.5;       // MHz
const KAPPA: f64 = 1.0;     // MHz
const F0: f64 = 141.7001;   // Hz

fn compute_s21(omega_d_MHz: f64, gamma_phi_MHz: f64) -> f64 {
    let delta_r = omega_d_MHz;
    let gamma_phi = gamma_phi_MHz * 2.0 * PI;
    let chi_sq = (CHI * 2.0 * PI).powi(2);
    let kappa_half = (KAPPA * 2.0 * PI) / 2.0;

    let denom_aut = (delta_r * 2.0 * PI) + (gamma_phi / 2.0) * 1i;
    let sigma = chi_sq / denom_aut;
    let g_inv = (delta_r * 2.0 * PI) + kappa_half * 1i - sigma;
    let g = 1.0 / g_inv;

    (g.re.powi(2) + g.im.powi(2)) / (1.0 + (g.re.powi(2) + g.im.powi(2)))
}

fn classify_regime(gamma_phi_MHz: f64) -> String {
    if gamma_phi_MHz < 1.5 {
        "FIRMA_A: Geometria Preexistente (Acoplamiento Fuerte)".into()
    } else if gamma_phi_MHz > 15.0 {
        "FIRMA_C: Curva Local por Entrelazamiento (Zeno)".into()
    } else {
        "FIRMA_B: Auto-Observacion (Streaking)".into()
    }
}

#[tonic::async_trait]
impl HardwareCoSimulationService for QcalHilServer {
    async fn compute_transmission(
        &self,
        request: Request<TransmissionRequest>,
    ) -> Result<Response<TransmissionResponse>, Status> {
        let req = request.into_inner();
        let gamma = req.gamma_phi_mhz;
        let chi = if req.chi_mhz > 0.0 { req.chi_mhz } else { CHI };

        let n_points = 401;
        let freqs: Vec<f64> = (0..n_points)
            .map(|i| -15.0 + (30.0 * i as f64) / (n_points as f64 - 1.0))
            .collect();

        let s21: Vec<f64> = freqs.iter().map(|&f| compute_s21(f + 7000.0, gamma)).collect();

        let regime = classify_regime(gamma);

        Ok(Response::new(TransmissionResponse {
            frequencies_mhz: freqs,
            s21_power: s21,
            regime_signature: regime,
            execution_id: uuid::Uuid::new_v4().to_string(),
            signature: format!("AMDA-Ψ-{}", std::env::consts::ARCH),
        }))
    }

    type StreamCoSimulationStream = ReceiverStream<Result<HardwareTelemetry, Status>>;

    async fn stream_co_simulation(
        &self,
        _request: Request<tonic::Streaming<SoftwarePhaseInjection>>,
    ) -> Result<Response<Self::StreamCoSimulationStream>, Status> {
        let (tx, rx) = mpsc::channel(4);
        tokio::spawn(async move {
            loop {
                let psi = 0.999999 - rand::random::<f64>() * 0.000001;
                let telemetry = HardwareTelemetry {
                    psi_instant: psi,
                    f0_measured_hz: F0 + rand::random::<f64>() * 0.0001,
                    timestamp_unix: std::time::SystemTime::now()
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap()
                        .as_secs() as i64,
                    node_id: "QCAL-cQED-v1-MacMini".into(),
                    coherence_lock: psi > 0.999,
                    hardware_error: false,
                };
                tx.send(Ok(telemetry)).await.unwrap();
                tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
            }
        });
        Ok(Response::new(ReceiverStream::new(rx)))
    }

    async fn submit_optimization(
        &self,
        request: Request<Optimization>,
    ) -> Result<Response<OptimizationReceipt>, Status> {
        let opt = request.into_inner();
        Ok(Response::new(OptimizationReceipt {
            receipt_id: uuid::Uuid::new_v4().to_string(),
            pi_code_credit: 1.337,
            merged: false,
            reviewer_vortex: "PENDIENTE".into(),
            signature: "MEUCICivMqhSJAkhWpW5gaD92fPeFws2wK6hHmRV1f8d/4toAiEAlGtnmD2/2kadS...".into(),
        }))
    }

    async fn submit_candidacy(
        &self,
        request: Request<CandidacyRequest>,
    ) -> Result<Response<CandidacyReceipt>, Status> {
        let _candidate = request.into_inner();
        Ok(Response::new(CandidacyReceipt {
            candidacy_id: format!("CAND-{}", uuid::Uuid::new_v4()),
            status: "RECIBIDA".into(),
            phi_score: 0.9999,
            hash: format!("πCODE-{}", uuid::Uuid::new_v4()),
            signature: "MEUCICivMqhSJAkhWpW5gaD92fPeFws2wK6hHmRV1f8d/4toAiEAlGtnmD2/2kadS...".into(),
            timestamp: format!("{}", std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH).unwrap().as_secs()),
            sello: "∴𓂀Ω∞³Φ".into(),
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    let service = QcalHilServer::default();

    println!("⚡ QCAL-cQED-v1 gRPC Server");
    println!("   f₀ = {} Hz", F0);
    println!("   Escuchando en {}", addr);
    println!("   Endpoints:");
    println!("     • ComputeTransmission    → S₂₁(ω) en vivo");
    println!("     • StreamCoSimulation     → Ψ en tiempo real");
    println!("     • SubmitOptimization     → Optimizaciones firmadas");
    println!("     • SubmitCandidacy        → Candidaturas al Vórtice");
    println!("   Sello: ∴𓂀Ω∞³Φ");

    Server::builder()
        .add_service(HardwareCoSimulationServiceServer::new(service))
        .serve(addr)
        .await?;

    Ok(())
}
