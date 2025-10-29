//! Git operations (T2.1: 2 weeks, 12 tasks)

pub mod clone;
pub mod commit;
pub mod init;
pub mod open;
pub mod repo;
pub mod submodule;
pub mod sync;

pub use init::init_repo;
pub use open::open_repo;
pub use repo::PaniniRepo;
