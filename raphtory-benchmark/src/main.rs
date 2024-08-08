use raphtory::{
    algorithms::motifs::{self, global_temporal_three_node_motifs::{global_temporal_three_node_motif, temporal_three_node_motif_multi}}, db::graph::graph::Graph, graph_loader::source::csv_loader::CsvLoader, prelude::*
};
// use raphtory::graph_loader;

use serde::Deserialize;
use std::{env, fs::File, io::Write, path::Path, time::Instant};

#[derive(Deserialize, std::fmt::Debug)]
struct Edge {
    src: u64,
    dst: u64,
    time: i64,
}

fn run_motifs_multi(file: &mut File) {
    for i in 0..10 {
        let deltas: Vec<i64> = (0..i)
            .flat_map(|j| (0..24).map(move |k| (i * 86400 + k * 3600) as i64))
            .collect();
        let now = Instant::now();
        let g = load_graph();
        let motifs = temporal_three_node_motif_multi(&g, deltas, None);
        writeln!(file, "{},{}", (i+1) * 24, now.elapsed().as_millis())
            .expect("Failed to write to file");
    }
}

fn run_motifs_multi_small(file: &mut File) {
    for i in 0..24 {
        let deltas : Vec<i64> = (0..i)
        .map(|k| k * 3600)
        .collect();
        let now = Instant::now();
        let g = load_graph();
        let motifs = temporal_three_node_motif_multi(&g, deltas, None);
        writeln!(file, "{},{}", (i+1), now.elapsed().as_millis())
            .expect("Failed to write to file");
    }
}

fn load_graph() -> Graph {
    let args: Vec<String> = env::args().collect();
    let data_dir = Path::new(args.get(1).expect("No NFT data directory provided"));
    let g = Graph::new();
    CsvLoader::new(data_dir)
        .set_delimiter(" ")
        .set_header(false)
        .load_into_graph(&g, |e: Edge, g| {
            g.add_edge(e.time, e.src, e.dst, NO_PROPS, None)
                .expect("Failed to add edge");
        })
        .expect("Failed to load graph from encoded data files");
    g
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let ex_string = args.get(2).expect("No experiment string provided");
    let file_str = "raphtory-output".to_owned() + ex_string + ".dat";
    let mut file = File::create(file_str)
        .expect("Failed to create file");

    run_motifs_multi_small(&mut file);
}