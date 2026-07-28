/* 
   Plan for AJAX-based LMS Admin transformation
   
   1. UI Transformation:
      - Replace all <form> actions that lead to redirects with AJAX submission handlers using Fetch API.
      - Use data attributes on forms to identify success callbacks (e.g., refreshing specific components).
      - Replace all browser 'confirm()' calls with custom modals using an event-driven approach.
      - Add a toast manager in JS that listens for successful operation signals from AJAX.
   
   2. Backend Enhancements:
      - Add new API-like endpoints for partial updates (partial HTML partials).
      - Optimize `select_related` and `prefetch_related` in `aidadminpage` view to fix N+1.
      - Revise assignment logic to handle selective quizzes:
        - Add 'selected_quizzes' list to the POST request.
        - Validate assignments and prevent duplicates using a unique key or explicit lookup.
   
   3. UI/UX:
      - Use localStorage to save the active sidebar section and possibly open modals/accordions.
      - Add spinner overlays/button disabled states on all forms during requests.
*/
