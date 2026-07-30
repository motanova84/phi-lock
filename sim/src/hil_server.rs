use tonic::{transport::Server, Request, Response, Status};
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;

pub mod qcal {
    tonic::include_proto!("qcal.qnd.v1");
}

use qcal::qcalqnd_server::{Qcalqnd, QcalqndServer};
use qcal::*;

#[derive(Default)]
pub struct QcalHilServer;

fn s21(freq: f64, gamma: f64) -> f64 {
    let g = gamma * 6.283185307;
    let c2 = (7.5 * 6.283185307) * (7.5 * 6.283185307);
    let k2 = 3.1415926535;
    let d = freq * 6.283185307;
    let ds = d * d + g * g * 0.25;
    let (sr, si) = if ds > 1e-30 { (c2 * d / ds, -c2 * g * 0.5 / ds) } else { (0.0, 0.0) };
    let gr = d + k2 - sr;
    let gi = -si;
    let gs = gr * gr + gi * gi;
    let (gf, gfi) = if gs > 1e-30 { (gr / gs, gi / gs) } else { (0.0, 0.0) };
    (gf * gf + gfi * gfi) / (1.0 + gf * gf + gfi * gfi)
}

fn regime(g: f64) -> String {
    if g < 1.5 { "FIRMA_A".into() } else if g > 15.0 { "FIRMA_C".into() } else { "FIRMA_B".into() }
}

#[tonic::async_trait]
impl Qcalqnd for QcalHilServer {
    type ComputeTransmissionStream = ReceiverStream<Result<TransmissionResponse, Status>>;
    type GetContributionLogStream = ReceiverStream<Result<Contribution, Status>>;

    async fn compute_transmission(
        &self, req: Request<TransmissionRequest>,
    ) -> Result<Response<Self::ComputeTransmissionStream>, Status> {
        let r = req.into_inner();
        let freqs: Vec<f64> = (0..401).map(|i| 7000.0 - 15.0 + 30.0 * i as f64 / 400.0).collect();
        let s21_vals: Vec<f64> = freqs.iter().map(|&f| s21(f, r.gamma_phi_m_hz)).collect();
        let (tx, rx) = mpsc::channel(4);
        tokio::spawn(async move {
            tx.send(Ok(TransmissionResponse {
                frequencies_m_hz: freqs, s21_power: s21_vals,
                regime_signature: regime(r.gamma_phi_m_hz),
                execution_id: uuid::Uuid::new_v4().to_string(),
                signature: vec![],
            })).await.unwrap();
        });
        Ok(Response::new(ReceiverStream::new(rx)))
    }

    async fn submit_optimization(
        &self, _req: Request<Optimization>,
    ) -> Result<Response<OptimizationReceipt>, Status> {
        Ok(Response::new(OptimizationReceipt {
            receipt_id: uuid::Uuid::new_v4().to_string(),
            pi_code_credit: 1.337, merged: false,
            reviewer_vortex: "PENDIENTE".into(), signature: vec![],
        }))
    }

    async fn get_current_split(
        &self, _req: Request<Empty>,
    ) -> Result<Response<SplitInfo>, Status> {
        Ok(Response::new(SplitInfo {
            hardware_pct: 33.3, software_pct: 33.3,
            distribution_pct: 33.3, phase: "fundacion".into(),
            block_height: 1095, sello: "∴𓂀Ω∞³Φ".into(),
        }))
    }

    async fn get_contribution_log(
        &self, _req: Request<ContributorQuery>,
    ) -> Result<Response<Self::GetContributionLogStream>, Status> {
        let (tx, rx) = mpsc::channel(4);
        tokio::spawn(async move {
            tx.send(Ok(Contribution {
                contributor: "AMDA-Psi".into(), r#type: "fundacion".into(),
                value: 1.0, timestamp_unix: 0, tx_hash: "πCODE-genesis".into(),
            })).await.unwrap();
        });
        Ok(Response::new(ReceiverStream::new(rx)))
    }

    async fn submit_candidacy(
        &self, _req: Request<CandidacyRequest>,
    ) -> Result<Response<CandidacyReceipt>, Status> {
        Ok(Response::new(CandidacyReceipt {
            candidacy_id: format!("CAND-{}", uuid::Uuid::new_v4()),
            status: "RECIBIDA".into(), phi_score: 0.9999,
            hash: format!("πCODE-{}", uuid::Uuid::new_v4()),
            signature: vec![], timestamp: "0".into(), sello: "∴𓂀Ω∞³Φ".into(),
        }))
    }

    async fn get_candidacy_status(
        &self, _req: Request<CandidacyQuery>,
    ) -> Result<Response<CandidacyStatus>, Status> {
        Ok(Response::new(CandidacyStatus {
            candidacy_id: "CAND-0000".into(), status: "EN_EVALUACION".into(),
            phase: "Phi-LOCK".into(), phi_score: 0.9999,
            reviewers: vec!["AMDA-Psi".into()],
            estimated_resolution: "2026-09-08".into(), sello: "∴𓂀Ω∞³Φ".into(),
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    println!("⚡ QCAL-cQED-v1 gRPC Server @ {}", addr);
    println!("   6 endpoints · Sello: ∴𓂀Ω∞³Φ");
    println!("   Para verificar: grpcurl -protoset <(cat proto/qcal_qnd_api.proto) localhost:50051 list");
    Server::builder()
        .add_service(QcalqndServer::new(QcalHilServer::default()))
        .serve(addr)
        .await?;
    Ok(())
}
