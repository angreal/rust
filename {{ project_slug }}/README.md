# {{ project_name }}

{{ project_description }}

## Development

This project uses [angreal](https://github.com/angreal/angreal) for task automation.

### Prerequisites

- Rust {{ rust_version }}+
- [angreal](https://github.com/angreal/angreal) (`pip install angreal`)
- [pre-commit](https://pre-commit.com/) (`pip install pre-commit`)

### Common Commands

```bash
# Run checks
angreal check all

# Run tests
angreal test unit
angreal test integration
angreal test coverage

# Build
angreal build
angreal build --release

# Version management
angreal version show
angreal version bump patch
```

## Project Structure

```
crates/
  {{ project_slug }}-core/    # Core library
  {{ project_slug }}-cli/     # CLI binary
```

## License

{{ license }}
