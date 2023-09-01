class MinecraftVersion:
    def __init__(self, version_str):
        self.version_str = version_str
        self.major, self.minor, self.patch = self.parse_version(version_str)

    def parse_version(self, version_str):
        try:
            parts = version_str.split('.')
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2]) if len(parts) > 2 else 0 #  First version of minors do not have patch
            
            return major, minor, patch
        except (IndexError, ValueError):
            raise ValueError("Invalid version format")

    def __lt__(self, other):
        return (
            self.major < other.major or
            (self.major == other.major and self.minor < other.minor) or
            (self.major == other.major and self.minor == other.minor and self.patch < other.patch)
        )

    def __gt__(self, other):
        return other < self

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __str__(self):
        return self.version_str