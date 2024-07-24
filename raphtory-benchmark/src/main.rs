use raphtory::{
    algorithms::motifs::{self, global_temporal_three_node_motifs::{global_temporal_three_node_motif, temporal_three_node_motif_multi}}, db::graph::graph::Graph, graph_loader::source::csv_loader::CsvLoader, prelude::*
};
// use raphtory::graph_loader;

use serde::Deserialize;
use std::{env, path::Path, time::Instant};

#[derive(Deserialize, std::fmt::Debug)]
struct Edge {
    src: u64,
    dst: u64,
    time: i64,
}

fn run_motifs_single() {
    let args: Vec<String> = env::args().collect();
    let g = load_graph();

    let now2 = Instant::now();

    let motifs = global_temporal_three_node_motif(&g, 86400, None);
    println!(
        "Counting motifs took {} milliseconds",
        now2.elapsed().as_millis()
    );
}

fn run_motifs_multi() {
    for i in 0..10 {
        let deltas: Vec<i64> = (0..i)
            .flat_map(|j| (0..24).map(move |k| (i * 86400 + k * 3600) as i64))
            .collect();
        let now = Instant::now();
        let g = load_graph();
        let motifs = temporal_three_node_motif_multi(&g, deltas, None);
        println!("{},{}",(i+1) * 24, now.elapsed().as_millis())
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
    for _ in 0..10 {
        run_motifs_multi();
    }
}