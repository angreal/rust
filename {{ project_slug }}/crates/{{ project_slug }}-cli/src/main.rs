use clap::Parser;

#[derive(Parser)]
#[command(
    name = "{{ project_slug }}",
    version,
    about = "{{ project_description }}"
)]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(clap::Subcommand)]
enum Commands {
    /// Display version information
    Version,
}

fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    let cli = Cli::parse();

    match cli.command {
        Some(Commands::Version) => {
            println!("{} {}", env!("CARGO_PKG_NAME"), env!("CARGO_PKG_VERSION"));
        }
        None => {
            println!("{{ project_name }} v{}", env!("CARGO_PKG_VERSION"));
            println!("Run with --help for usage information.");
        }
    }

    Ok(())
}
