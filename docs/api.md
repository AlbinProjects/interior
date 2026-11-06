# REST API Documentation

Base URL: `http://localhost:8000/api`

---

## 1. Rooms & Ingestion

### `POST /api/rooms/upload`
Uploads and validates a room image, executing the 6-stage Room Analyzer pipeline.
* **Content-Type**: `multipart/form-data`
* **Parameters**:
  * `file`: Binary image file (JPG, PNG, WEBP)
  * `project_id` *(optional)*: Existing project ID
* **Response**: `RoomUploadResponse` with detected objects, depth map URL, and segmentation overlay URL.

### `GET /api/rooms/{id}/analysis`
Retrieves spatial graph and detected furniture items for a room upload.

---

## 2. Design Generation & Inpainting

### `POST /api/designs/generate`
Generates a structure-preserving redesigned room.
* **Body (JSON)**:
```json
{
  "project_id": "proj_123",
  "room_upload_id": "room_456",
  "room_type": "living_room",
  "selected_style": "modern",
  "selected_palette": "warm_neutral",
  "budget_target": 75000,
  "user_requirements": "Keep TV unit, add plants and warmer lighting",
  "structure_preservation_level": "balanced"
}
```
* **Response**: `DesignVersionResponse` with generated image URL, structured plan, and budget estimate.

### `POST /api/designs/{id}/edit`
Executes object-level mask inpainting.
* **Body (JSON)**:
```json
{
  "design_version_id": "ver_789",
  "object_label": "sofa",
  "action": "replace",
  "prompt": "Replace with dark green modern velvet sofa",
  "bbox": { "x_min": 0.2, "y_min": 0.45, "x_max": 0.8, "y_max": 0.85 }
}
```

### `GET /api/designs/{id}`
Returns full design version details, generated image, and design blueprint.

### `GET /api/designs/project/{project_id}/versions`
Returns all design version iterations for a given project.

---

## 3. Conversational AI Designer

### `POST /api/chat`
Sends natural language modification instructions to the AI designer.
* **Body (JSON)**:
```json
{
  "project_id": "proj_123",
  "design_version_id": "ver_789",
  "message": "Make the sofa beige and lighting warmer"
}
```
* **Response**: `ChatMessageResponse` containing assistant reply, executed modification, and new `DesignVersion` details.

### `GET /api/chat/project/{project_id}`
Returns multi-turn chat history.

---

## 4. Budget & Shopping Catalog

### `GET /api/budget/{design_id}`
Returns calculated bill of materials with price ranges and category subtotals.

### `GET /api/budget/{design_id}/furniture`
Returns itemized shopping catalog.

---

## 5. Projects

### `POST /api/projects`
Creates a new interior design project container.

### `GET /api/projects`
Lists saved projects with thumbnails and latest version counters.

### `GET /api/projects/{id}`
Retrieves complete project history, rooms, and design versions.

### `DELETE /api/projects/{id}`
Deletes a project and associated media.
