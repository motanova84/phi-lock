fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("../proto/qcal_qnd_api.proto")?;
    Ok(())
}
