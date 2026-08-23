// VULNERABLE: notifyNeedTermination()
void VM::notifyNeedTermination() {
    // [!] VOID START: Setting state from the Main Thread
    setHasTerminationRequest(true); 
    
    // In the gap between these two lines, a Worker Thread 
    // can call clearHasTerminationRequest(), 
    // creating a "State Vacuum."
    
    m_traps.trigger(VMTraps::NeedTermination);
}
