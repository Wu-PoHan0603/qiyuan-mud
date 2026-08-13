class DebugSystem:
    """Coordinates debug actions without depending on Pygame drawing APIs."""

    def toggle(self, state):
        enabled = state.toggle()
        state.set_message(
            "Debug mode enabled" if enabled else "Debug mode disabled"
        )
        return enabled

    def report(self, state, message):
        state.set_message(message)
        return message

    def build_lines(self, state, scene_name, player, fps):
        if not state.enabled:
            return ()

        lines = [
            f"FPS: {fps:.1f}",
            f"Scene: {scene_name or 'NONE'}",
        ]
        if player is not None:
            lines.extend(
                (
                    f"Player: {player.name}",
                    f"Level: {player.level}",
                    f"Realm: {player.realm}",
                    f"HP/MP: {player.hp}/{player.max_hp}  "
                    f"{player.mp}/{player.max_mp}",
                )
            )
        if state.last_message:
            lines.append(state.last_message)
        return tuple(lines)

