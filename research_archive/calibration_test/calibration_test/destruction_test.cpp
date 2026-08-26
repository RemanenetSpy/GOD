void HTMLMediaElement::prepareForDestruction()
{
    // The "Body" prepares to die
    m_networkState = NETWORK_EMPTY;
    m_readyState = HAVE_NOTHING;

    // Potential Void: If the m_player is disconnected here, 
    // but a callback is already scheduled in the event loop...
    if (m_player) {
        m_player->invalidate();
        m_player = nullptr;
    }

    // [!] DANGER: Stop all active timers. 
    // If a timer fires AFTER m_player is null, it's a 0.00 Density event.
    stopPeriodicTimers();
    m_resourceSelectionTimer.stop();
}
