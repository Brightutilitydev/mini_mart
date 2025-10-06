import { AxiosError } from 'axios'

class CustomAppError extends AxiosError {
  constructor(error: AxiosError) {
    super(
      (error?.response?.data as { message: string }).message
        ? (error?.response?.data as { message: string }).message
        : undefined
    )
    this.name = 'Request Error'
    this.code = error.code
    this.response = error.response
    this.config = error.config
  }
}

export default CustomAppError
